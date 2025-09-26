import asyncio
import json
import time
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

# Default modern viewport set (can be overridden by caller)
DEFAULT_VIEWPORTS: Dict[str, Dict[str, Any]] = {
    "desktop_hd": {"width": 1920, "height": 1080, "device_scale_factor": 1, "is_mobile": False},
    "mobile_modern": {"width": 390, "height": 844, "device_scale_factor": 3, "is_mobile": True},
}

HASH_ATTR = "data-el-hash"

############################################################
# Utility hashing & DOM instrumentation (executed in page) #
############################################################

HASH_JS = f"""
(() => {{
  // Stable hash function (SHA-1 like simplified)
  function sha1(str) {{
    // Minimal SHA-1 implementation substitute using SubtleCrypto when available
    if (window.crypto && window.crypto.subtle && window.TextEncoder) {{
      return window.crypto.subtle.digest('SHA-1', new TextEncoder().encode(str)).then(buf => {{
        return Array.from(new Uint8Array(buf)).map(x=>x.toString(16).padStart(2,'0')).join('');
      }});
    }} else {{
      // Fallback super simple (non-cryptographic) hash
      let h = 0; for (let i=0;i<str.length;i++) {{ h = ((h<<5)-h) + str.charCodeAt(i); h|=0; }}
      return Promise.resolve('f'+(h >>> 0).toString(16));
    }}
  }}

  function nodeSignature(el) {{
    if (!(el instanceof Element)) return '';
    const tag = el.tagName.toLowerCase();
    const id = el.id ? ('#'+el.id) : '';
    const cls = el.classList.length ? ('.'+Array.from(el.classList).sort().join('.')) : '';
    const role = el.getAttribute('role') || '';
    const aria = el.getAttributeNames().filter(n=>n.startsWith('aria-')).sort().map(n=>n+':'+el.getAttribute(n)).join('|');
    let text = '';
    if (['script','style','noscript'].indexOf(tag) === -1) {{
      text = (el.textContent||'').trim().replace(/\s+/g,' ').slice(0,80);
    }}
    // build structural path
    let pathParts = [];
    let cur = el;
    while (cur && cur.nodeType === 1 && pathParts.length < 40) {{
      const parent = cur.parentElement;
      let nth = 1;
      if (parent) {{
        let sib = parent.firstElementChild;
        while (sib && sib !== cur) {{
          if (sib.tagName === cur.tagName) nth++;
          sib = sib.nextElementSibling;
        }}
      }}
      pathParts.push(cur.tagName.toLowerCase()+':'+nth);
      cur = parent;
    }}
    const structuralPath = pathParts.reverse().join('>');
    return [structuralPath, tag, id, cls, role, aria, text].join('|');
  }}

  async function hashAll() {{
    const all = Array.from(document.querySelectorAll('html, body, body *'));
    const promises = all.map(async el => {{
      const sig = nodeSignature(el);
      const h = await sha1(sig);
      el.setAttribute('{HASH_ATTR}', h);
    }});
    await Promise.all(promises);
  }}

  if (!window.__HASHING_INITIALIZED__) {{
    window.__HASHING_INITIALIZED__ = true;
    window.__rehashDOM = hashAll;
    window.__computeElementHash = async function(sel) {{
      const el = document.querySelector(sel);
      if (!el) return null;
      const sig = nodeSignature(el);
      return sha1(sig);
    }};
  }}

  return hashAll().then(()=>true);
}})();
"""

RESOLVE_ELEMENT_JS = f"""
(selector, strategy) => {{
  if (strategy === 'css') {{
    const els = Array.from(document.querySelectorAll(selector));
    return els.length === 1 ? els[0].getAttribute('{HASH_ATTR}') : null;
  }} else if (strategy === 'hash') {{
    const el = document.querySelector('[{HASH_ATTR}="'+selector+'"]');
    return el ? el.getAttribute('{HASH_ATTR}') : null;
  }} else if (strategy === 'xpath') {{
    try {{
      const r = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
      if (r.singleNodeValue && r.singleNodeValue.nodeType === 1) {{
        return r.singleNodeValue.getAttribute('{HASH_ATTR}');
      }}
    }} catch(e) {{ return null; }}
    return null;
  }} else if (strategy === 'auto') {{
    // attempt css, then xpath, then assume it's already a hash
    const cssTry = (()=>{{
      try {{ const els = document.querySelectorAll(selector); return els.length===1 ? els[0] : null; }} catch(e) {{ return null; }}
    }})();
    if (cssTry) return cssTry.getAttribute('{HASH_ATTR}');
    try {{
      const r = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
      if (r.singleNodeValue && r.singleNodeValue.nodeType === 1) return r.singleNodeValue.getAttribute('{HASH_ATTR}');
    }} catch(e) {{}}
    const el = document.querySelector('[{HASH_ATTR}="'+selector+'"]');
    return el ? el.getAttribute('{HASH_ATTR}') : null;
  }}
  return null;
}}"""

APPLY_ACTION_JS = f"""
(hashValue, action) => {{
  const el = document.querySelector('[{HASH_ATTR}="'+hashValue+'"]');
  if (!el) return {{status:'not_found'}};
  const t = action.type;
  try {{
    if (t === 'set_attribute') {{
      const kv = action.value || {{}};
      Object.entries(kv).forEach(([k,v]) => {{ if (v is null || v === null) el.removeAttribute(k); else el.setAttribute(k, v); }});
    }} else if (t === 'remove_attribute') {{
      const names = Array.isArray(action.value) ? action.value : [action.value];
      names.filter(Boolean).forEach(n => el.removeAttribute(n));
    }} else if (t === 'replace_inner_html') {{
      el.innerHTML = action.value || '';
    }} else if (t === 'replace_outer_html') {{
      el.outerHTML = action.value || '';
    }} else if (t === 'set_text') {{
      el.textContent = action.value || '';
    }} else if (t === 'append_child') {{
      const tmp = document.createElement('div');
      tmp.innerHTML = action.value || '';
      Array.from(tmp.childNodes).forEach(n=>el.appendChild(n));
    }} else if (t === 'insert_before') {{
      const tmp = document.createElement('div');
      tmp.innerHTML = action.value || '';
      const parent = el.parentNode;
      if (parent) Array.from(tmp.childNodes).forEach(n=>parent.insertBefore(n, el));
    }} else if (t === 'insert_after') {{
      const tmp = document.createElement('div');
      tmp.innerHTML = action.value || '';
      const parent = el.parentNode;
      if (parent) Array.from(tmp.childNodes).reverse().forEach(n=>parent.insertBefore(n, el.nextSibling));
    }} else {{
      return {{status:'unknown_action'}};
    }}
    return {{status:'ok'}};
  }} catch(e) {{
    return {{status:'error', message: e.message}};
  }}
}}"""

GET_OUTER_HTML_JS = f"""
(hashValue) => {{
  const el = document.querySelector('[{HASH_ATTR}="'+hashValue+'"]');
  return el ? el.outerHTML : null;
}}"""

############################################
# Core capture & patch application helpers #
############################################

async def _instrument_dom(page):
    await page.add_init_script(HASH_JS)
    # If page already loaded past init, explicitly run script
    try:
        await page.evaluate(HASH_JS)
    except Exception:
        pass

async def _capture_accessibility(page):
    try:
        return await page.accessibility.snapshot(interesting_only=False)
    except Exception:
        return None

async def _safe_wait(page, wait_for: str, settle_ms: int):
    try:
        await page.wait_for_load_state(wait_for, timeout=30000)
    except PWTimeoutError:
        pass
    await page.wait_for_timeout(settle_ms)

async def _screenshot_multi(page, out_dir: Path, viewports: Dict[str, Dict[str, Any]]):
    shots = {}
    for name, vp in viewports.items():
        try:
            await page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
            await page.wait_for_timeout(250)
            shot_path = out_dir / f"{name}.png"
            await page.screenshot(path=str(shot_path), full_page=True)
            shots[name] = str(shot_path)
        except Exception:
            shots[name] = None
    return shots

async def _resolve_element_hash(page, locator: Dict[str, Any]) -> Optional[str]:
    strategy = locator.get('strategy', 'auto')
    value = locator.get('value')
    if not value:
        return None
    return await page.evaluate(RESOLVE_ELEMENT_JS, value, strategy)

async def _apply_action(page, hash_value: str, action: Dict[str, Any]) -> Dict[str, Any]:
    return await page.evaluate(APPLY_ACTION_JS, hash_value, action)

async def _get_outer_html(page, hash_value: str) -> Optional[str]:
    return await page.evaluate(GET_OUTER_HTML_JS, hash_value)

############################################
# Public main function                    #
############################################

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
    """Load a page, capture BEFORE, apply patches live, capture AFTER.

    patches: list of patch descriptors.
    Each patch: {
        "locator": {"strategy":"css|xpath|hash|auto", "value":"..."},
        "action": {"type": "set_attribute|replace_inner_html|...", "value": ...},
        "verify": {"must_contain": [...], "must_not_contain": [...]},
        "id": "optional_id"
    }
    """
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
        except PWTimeoutError:
            manifest['before']['status'] = 'timeout'
        except Exception as e:
            manifest['before']['status'] = f"error:{type(e).__name__}"
        await _safe_wait(page, wait_for, settle_ms)
        await _instrument_dom(page)

        # BEFORE capture
        try:
            before_html = await page.content()
            (out_root / 'before' / 'page.html').write_text(before_html, encoding='utf-8', errors='ignore')
            if evaluate_accessibility:
                a11y = await _capture_accessibility(page)
                if a11y is not None:
                    (out_root / 'before' / 'a11y.json').write_text(json.dumps(a11y, ensure_ascii=False, indent=2))
        except Exception:
            pass
        manifest['before']['screenshots'] = await _screenshot_multi(page, out_root / 'before', vp)

        # Apply patches (in current viewport context; DOM changes persist across resizes)
        for idx, patch in enumerate(patches):
            p_id = patch.get('id') or f"patch_{idx+1:03d}"
            entry = {
                'id': p_id,
                'locator': patch.get('locator'),
                'action_type': patch.get('action', {}).get('type'),
                'status': 'pending'
            }
            try:
                resolved_hash = await _resolve_element_hash(page, patch.get('locator', {}))
                entry['resolved_hash'] = resolved_hash
                if not resolved_hash:
                    entry['status'] = 'not_found'
                    manifest['patches'].append(entry)
                    continue
                before_outer = await _get_outer_html(page, resolved_hash)
                if before_outer:
                    (out_root / 'patches' / f"{p_id}_before.html").write_text(before_outer, encoding='utf-8', errors='ignore')
                result = await _apply_action(page, resolved_hash, patch.get('action', {}))
                entry['apply_result'] = result
                if result.get('status') == 'ok':
                    # Re-hash entire DOM (simpler) after each patch to keep hashes stable references
                    try:
                        await page.evaluate("window.__rehashDOM && window.__rehashDOM()")
                    except Exception:
                        pass
                    after_outer = await _get_outer_html(page, resolved_hash)  # may differ if outer replaced
                    if after_outer:
                        (out_root / 'patches' / f"{p_id}_after.html").write_text(after_outer, encoding='utf-8', errors='ignore')
                    # Verification
                    ver = patch.get('verify') or {}
                    ver_status = 'ok'
                    if ver:
                        if ver.get('must_contain'):
                            for s in ver['must_contain']:
                                if s not in (after_outer or ''):
                                    ver_status = 'fail_contains'
                                    break
                        if ver_status == 'ok' and ver.get('must_not_contain'):
                            for s in ver['must_not_contain']:
                                if s in (after_outer or ''):
                                    ver_status = 'fail_not_contains'
                                    break
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
                a11y2 = await _capture_accessibility(page)
                if a11y2 is not None:
                    (out_root / 'after' / 'a11y.json').write_text(json.dumps(a11y2, ensure_ascii=False, indent=2))
        except Exception:
            pass
        manifest['after']['screenshots'] = await _screenshot_multi(page, out_root / 'after', vp)

        await context.close()
        await browser.close()

    manifest_path = Path(out_dir) / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    if verbose:
        print(json.dumps(manifest, indent=2)[:1200])
    return manifest

############################################
# Synchronous wrapper & CLI               #
############################################

def run_capture_with_patches(**kwargs) -> Dict[str, Any]:
    return asyncio.run(capture_with_patches(**kwargs))

def _parse_patches_file(patches_file: str) -> List[Dict[str, Any]]:
    p = Path(patches_file)
    if not p.exists():
        raise FileNotFoundError(patches_file)
    data = json.loads(p.read_text(encoding='utf-8'))
    if isinstance(data, dict):
        return data.get('patches', [])
    return data


def main():
    ap = argparse.ArgumentParser(description="Live capture + patch application (before/after screenshots)")
    ap.add_argument('--url', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--patches', required=True, help='JSON file: array or {"patches": [...]}')
    ap.add_argument('--wait-for', default='networkidle')
    ap.add_argument('--settle-ms', type=int, default=2500)
    ap.add_argument('--no-a11y', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()

    patches = _parse_patches_file(args.patches)
    run_capture_with_patches(
        url=args.url,
        patches=patches,
        out_dir=args.out,
        wait_for=args.wait_for,
        settle_ms=args.settle_ms,
        evaluate_accessibility=not args.no_a11y,
        verbose=args.verbose
    )

if __name__ == '__main__':
    main()
