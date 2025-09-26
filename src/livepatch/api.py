import asyncio
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

from .constants import DEFAULT_VIEWPORTS
from .instrumentation import instrument_dom
from .capture import safe_wait, capture_accessibility, screenshot_multi
from .patch_actions import resolve_element_hash, apply_action, get_outer_html

async def capture_with_patches(
    url: str,
    patches: List[Dict[str, Any]],
    out_dir: str,
    viewports: Optional[Dict[str, Dict[str, Any]]] = None,
    wait_for: str = "networkidle",
    settle_ms: int = 2500,
    evaluate_accessibility: bool = True,
    verbose: bool = False
) -> Dict[str, Any]:
    t0 = time.time()
    out_root = Path(out_dir)
    (out_root / 'before').mkdir(parents=True, exist_ok=True)
    (out_root / 'after').mkdir(parents=True, exist_ok=True)
    (out_root / 'patches').mkdir(parents=True, exist_ok=True)

    vp = viewports or DEFAULT_VIEWPORTS

    manifest: Dict[str, Any] = {
        "url": url,
        "timestamp": int(t0),
        "viewports": list(vp.keys()),
        "before": {},
        "after": {},
        "patches": [],
        "meta": {
            "wait_for": wait_for,
            "settle_ms": settle_ms,
            "evaluate_accessibility": evaluate_accessibility
        }
    }

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        context = await browser.new_context(viewport={"width": 1280, "height": 800}, bypass_csp=True)
        page = await context.new_page()
        try:
            resp = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            manifest['before']['status'] = resp.status if resp else None
        except TimeoutError:
            manifest['before']['status'] = 'timeout'
        except Exception as e:
            manifest['before']['status'] = f"error:{type(e).__name__}"
        await safe_wait(page, wait_for, settle_ms)
        await instrument_dom(page)

        # BEFORE capture
        try:
            before_html = await page.content()
            (out_root / 'before' / 'page.html').write_text(before_html, encoding='utf-8', errors='ignore')
            if evaluate_accessibility:
                a11y = await capture_accessibility(page)
                if a11y is not None:
                    (out_root / 'before' / 'a11y.json').write_text(json.dumps(a11y, ensure_ascii=False, indent=2))
        except Exception:
            pass
        manifest['before']['screenshots'] = await screenshot_multi(page, out_root / 'before', vp)

        # Apply patches
        for idx, patch in enumerate(patches):
            p_id = patch.get('id') or f"patch_{idx+1:03d}"
            entry = {
                'id': p_id,
                'locator': patch.get('locator'),
                'action_type': patch.get('action', {}).get('type'),
                'status': 'pending'
            }
            try:
                resolved_hash = await resolve_element_hash(page, patch.get('locator', {}))
                entry['resolved_hash'] = resolved_hash
                if not resolved_hash:
                    entry['status'] = 'not_found'
                    manifest['patches'].append(entry)
                    continue
                before_outer = await get_outer_html(page, resolved_hash)
                if before_outer:
                    (out_root / 'patches' / f"{p_id}_before.html").write_text(before_outer, encoding='utf-8', errors='ignore')
                result = await apply_action(page, resolved_hash, patch.get('action', {}))
                entry['apply_result'] = result
                if result.get('status') == 'ok':
                    try:
                        await page.evaluate("window.__rehashDOM && window.__rehashDOM()")
                    except Exception:
                        pass
                    after_outer = await get_outer_html(page, resolved_hash)
                    if after_outer:
                        (out_root / 'patches' / f"{p_id}_after.html").write_text(after_outer, encoding='utf-8', errors='ignore')
                    ver = patch.get('verify') or {}
                    ver_status = 'ok'
                    if ver:
                        if ver.get('must_contain'):
                            for s in ver['must_contain']:
                                if s not in (after_outer or ''):
                                    ver_status = 'fail_contains'; break
                        if ver_status == 'ok' and ver.get('must_not_contain'):
                            for s in ver['must_not_contain']:
                                if s in (after_outer or ''):
                                    ver_status = 'fail_not_contains'; break
                    entry['verify_status'] = ver_status
                    entry['status'] = 'applied'
                else:
                    entry['status'] = result.get('status')
            except Exception as e:
                entry['status'] = 'error'
                entry['error'] = str(e)
            manifest['patches'].append(entry)

        # AFTER capture
        try:
            after_html = await page.content()
            (out_root / 'after' / 'page.html').write_text(after_html, encoding='utf-8', errors='ignore')
            if evaluate_accessibility:
                a11y2 = await capture_accessibility(page)
                if a11y2 is not None:
                    (out_root / 'after' / 'a11y.json').write_text(json.dumps(a11y2, ensure_ascii=False, indent=2))
        except Exception:
            pass
        manifest['after']['screenshots'] = await screenshot_multi(page, out_root / 'after', vp)

        await context.close()
        await browser.close()

    manifest_path = Path(out_dir) / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    if verbose:
        print(json.dumps(manifest, indent=2)[:1200])
    return manifest


def run_capture_with_patches(**kwargs) -> Dict[str, Any]:
    return asyncio.run(capture_with_patches(**kwargs))
