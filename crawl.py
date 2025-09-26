import asyncio
import json
import os
import re
import time
import hashlib
import argparse
import urllib.parse as urlparse
from pathlib import Path
from typing import Set, List, Dict

import tldextract
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser

from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

VIEWPORTS = {
    "mobile": {
        "width": 390, "height": 844,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    },
    "tablet": {
        "width": 820, "height": 1180,
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    },
    "desktop": {
        "width": 1920, "height": 1080,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
}

DEFAULT_WAIT = 3500  # ms after network idle to let things settle a bit more
NETWORK_IDLE_TIMEOUT = "networkidle"  # or "load" / "domcontentloaded"
SCROLL_STEPS = 8
SCROLL_PAUSE = 0.3  # seconds between scroll steps

def norm_url(href: str, base: str) -> str:
    if not href:
        return ""
    u = urlparse.urljoin(base, href)
    parsed = urlparse.urlparse(u)
    # strip fragments & common tracking params
    query = "&".join(sorted([p for p in parsed.query.split("&") if p and not p.startswith(("utm_", "fbclid", "gclid"))]))
    cleaned = parsed._replace(fragment="", query=query)
    return cleaned.geturl()

def is_same_site(seed: str, candidate: str) -> bool:
    s = tldextract.extract(seed)
    c = tldextract.extract(candidate)
    return (s.domain == c.domain and s.suffix == c.suffix)

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

async def polite_wait(page):
    # wait for network to go idle, then a bit more for late JS
    try:
        await page.wait_for_load_state(NETWORK_IDLE_TIMEOUT, timeout=30000)
    except PWTimeoutError:
        pass
    await page.wait_for_timeout(DEFAULT_WAIT)

async def autoscroll(page):
    try:
        for _ in range(SCROLL_STEPS):
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight/{});".format(SCROLL_STEPS))
            await asyncio.sleep(SCROLL_PAUSE)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(SCROLL_PAUSE)
        await page.evaluate("window.scrollTo(0, 0);")
    except Exception:
        pass

async def get_links(html: str, base: str) -> List[str]:
    out = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            u = norm_url(a.get("href"), base)
            if u.startswith("http"):
                out.append(u)
    except Exception:
        pass
    return out

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

class Robots:
    def __init__(self, seed_url: str):
        parsed = urlparse.urlparse(seed_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        self.rp = RobotFileParser()
        self._fetched = False
        try:
            self.rp.set_url(robots_url)
            self.rp.read()
            self._fetched = True
        except Exception:
            # network error -> treat as allow instead of implicit disallow_all that robotparser sets
            try:
                # reset disallow_all flag if set
                if getattr(self.rp, "disallow_all", False):
                    self.rp.disallow_all = False
            except Exception:
                pass

    def allowed(self, url: str, ua: str = "Mozilla/5.0"):
        try:
            allowed = self.rp.can_fetch(ua, url)
            # If fetch failed and robotparser decided disallow_all, override to allow
            if not self._fetched and getattr(self.rp, "disallow_all", False) and not getattr(self.rp, "allow_all", False):
                return True
            return allowed
        except Exception:
            return True

async def capture_page(context, url: str, out_dir: Path, viewport_name: str, vp_cfg: Dict) -> Dict:
    page = await context.new_page()
    # user agent override (optional)
    if vp_cfg.get("user_agent"):
        await page.set_extra_http_headers({"User-Agent": vp_cfg["user_agent"]})
    await page.set_viewport_size({"width": vp_cfg["width"], "height": vp_cfg["height"]})

    meta = {"viewport": viewport_name, "width": vp_cfg["width"], "height": vp_cfg["height"]}
    try:
        resp = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        meta["status"] = resp.status if resp else None
    except PWTimeoutError:
        meta["status"] = "timeout"
    except Exception as e:
        meta["status"] = f"error:{type(e).__name__}"
    # allow page to settle & lazy-load
    await polite_wait(page)
    await autoscroll(page)

    # full HTML
    try:
        html = await page.content()
    except Exception:
        html = ""

    # accessibility snapshot (Playwright)
    try:
        ax = await page.accessibility.snapshot(root=None, interesting_only=False)
    except Exception:
        ax = None

    # computed styles for the body (cheap proxy for theme/contrast context)
    try:
        css_vars = await page.evaluate("""() => {
          const s = getComputedStyle(document.body);
          return {
            color: s.color,
            backgroundColor: s.backgroundColor,
            fontSize: s.fontSize,
            lineHeight: s.lineHeight
          };
        }""")
    except Exception:
        css_vars = None

    # screenshot
    shot_path = out_dir / f"screenshot_{viewport_name}.png"
    try:
        await page.screenshot(path=str(shot_path), full_page=True)
    except Exception:
        pass

    # extract links
    links = await get_links(html, url)
    await page.close()
    return {
        "viewport": meta,
        "screenshot": str(shot_path),
        "links": links,
        "html_len": len(html),
        "html_path": str(out_dir / f"page.html"),
        "a11y_snapshot": ax,
        "computed_styles": css_vars,
        "status": meta.get("status")
    }, html

async def process_url(browser, url: str, out_root: Path, viewports: Dict) -> Dict:
    url_id = sha1(url)
    page_dir = out_root / url_id
    ensure_dir(page_dir)
    manifest = {
        "url": url,
        "url_id": url_id,
        "captured_at": int(time.time()),
        "viewports": [],
    }
    # separate contexts per viewport for clean emulation
    for name, vp in viewports.items():
        context = await browser.new_context(
            viewport={"width": vp["width"], "height": vp["height"]},
            device_scale_factor=1,
            is_mobile=(name == "mobile"),
            user_agent=vp.get("user_agent") or None,
            java_script_enabled=True,
            bypass_csp=True,
            locale="en-US",
        )
        try:
            vp_dir = page_dir / name
            ensure_dir(vp_dir)
            vp_capture, html = await capture_page(context, url, vp_dir, name, vp)
            # write HTML once per viewport (kept separate since DOM can differ)
            (vp_dir / "page.html").write_text(html, encoding="utf-8", errors="ignore")
            # a11y snapshot dump
            if vp_capture.get("a11y_snapshot") is not None:
                (vp_dir / "a11y.json").write_text(json.dumps(vp_capture["a11y_snapshot"], ensure_ascii=False, indent=2))
            # styles
            if vp_capture.get("computed_styles") is not None:
                (vp_dir / "styles.json").write_text(json.dumps(vp_capture["computed_styles"], ensure_ascii=False, indent=2))
            manifest["viewports"].append({
                "name": name,
                "screenshot": vp_capture["screenshot"],
                "html_path": vp_capture["html_path"],
                "a11y_path": str(vp_dir / "a11y.json") if vp_capture.get("a11y_snapshot") is not None else None,
                "styles_path": str(vp_dir / "styles.json") if vp_capture.get("computed_styles") is not None else None,
                "status": vp_capture["status"],
                "links": vp_capture["links"],
                "width": vp_capture["viewport"]["width"],
                "height": vp_capture["viewport"]["height"],
            })
        finally:
            await context.close()
    # page-level manifest
    (page_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    return manifest

async def crawl(seed: str, out_dir: str, depth: int, max_pages: int, concurrency: int, delay: float, same_site_only: bool, ignore_robots: bool, verbose: bool):
    out_root = Path(out_dir)
    ensure_dir(out_root)
    seen: Set[str] = set()
    q: List[Dict] = [{"url": seed, "depth": 0}]
    robots = Robots(seed) if not ignore_robots else None
    results = []
    skipped_counters = {"seen": 0, "offsite": 0, "robots": 0}

    sem = asyncio.Semaphore(concurrency)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        try:
            while q and len(results) < max_pages:
                batch = []
                # pull up to concurrency jobs
                while q and len(batch) < concurrency and len(results) + len(batch) < max_pages:
                    item = q.pop(0)
                    u, d = item["url"], item["depth"]
                    if u in seen:
                        skipped_counters["seen"] += 1
                        if verbose:
                            print(f"[skip:seen] {u}")
                        continue
                    if same_site_only and not is_same_site(seed, u):
                        skipped_counters["offsite"] += 1
                        if verbose:
                            print(f"[skip:offsite] {u}")
                        continue
                    if robots and not robots.allowed(u):
                        skipped_counters["robots"] += 1
                        if verbose:
                            print(f"[skip:robots] {u}")
                        continue
                    seen.add(u)
                    batch.append((u, d))

                async def worker(u, d):
                    async with sem:
                        try:
                            page_manifest = await process_url(browser, u, out_root, VIEWPORTS)
                            results.append(page_manifest)
                            # enqueue links from desktop view (if any) for next depth
                            next_links = []
                            for vp in page_manifest["viewports"]:
                                if vp["name"] == "desktop":
                                    next_links = vp.get("links") or []
                                    break
                            if d + 1 <= depth:
                                for ln in next_links:
                                    nu = norm_url(ln, u)
                                    if nu and nu not in seen:
                                        q.append({"url": nu, "depth": d + 1})
                        except Exception:
                            print(f"[error] processing {u}")
                            pass
                        finally:
                            await asyncio.sleep(delay)

                await asyncio.gather(*[worker(u, d) for (u, d) in batch])
        finally:
            await browser.close()

    # global crawl manifest
    manifest_obj = {
        "seed": seed,
        "out_dir": str(out_dir),
        "depth": depth,
        "max_pages": max_pages,
        "captured": len(results),
        "pages": results,
        "skipped": skipped_counters,
        "ignore_robots": ignore_robots,
        "same_site_only": same_site_only
    }
    (Path(out_dir) / "crawl_manifest.json").write_text(json.dumps(manifest_obj, ensure_ascii=False, indent=2))
    print(f"[done] captured {len(results)} pages → {out_dir}")
    if len(results) == 0:
        print("No pages captured. Potential reasons: 1) robots.txt disallowed seed (use --ignore-robots), 2) network/redirect issues, 3) all candidates filtered (off-site). Run with --verbose for details.")

def main():
    ap = argparse.ArgumentParser(description="Crawl webpages and collect multi-viewport screenshots + HTML for a11y.")
    ap.add_argument("seed", help="Seed URL, e.g., https://example.com")
    ap.add_argument("--out", default="data", help="Output directory")
    ap.add_argument("--depth", type=int, default=1, help="Crawl depth (BFS)")
    ap.add_argument("--max-pages", type=int, default=50, help="Max pages to capture")
    ap.add_argument("--concurrency", type=int, default=3, help="Concurrent pages")
    ap.add_argument("--delay", type=float, default=0.8, help="Politeness delay (seconds) between page fetches")
    ap.add_argument("--same-site-only", action="store_true", help="Restrict crawl to same registrable domain as seed")
    ap.add_argument("--ignore-robots", action="store_true", help="Ignore robots.txt (use responsibly)")
    ap.add_argument("--verbose", action="store_true", help="Verbose skip logging")
    args = ap.parse_args()

    # default to same-site-only for safety
    same = True if args.same_site_only or args.same_site_only is None else args.same_site_only
    asyncio.run(crawl(args.seed, args.out, args.depth, args.max_pages, args.concurrency, args.delay, same, args.ignore_robots, args.verbose))

if __name__ == "__main__":
    main()
