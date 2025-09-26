from .constants import HASH_ATTR

# JS snippets centralized for readability & reuse.

HASH_JS = f"""
(() => {{
  function sha1(str) {{
    if (window.crypto && window.crypto.subtle && window.TextEncoder) {{
      return window.crypto.subtle.digest('SHA-1', new TextEncoder().encode(str)).then(buf => {{
        return Array.from(new Uint8Array(buf)).map(x=>x.toString(16).padStart(2,'0')).join('');
      }});
    }} else {{
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
  text = (el.textContent||'').trim().replace(/\\s+/g,' ').slice(0,80);
    }}
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
(data) => {{
  const {{ selector, strategy }} = data || {{}};
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
(data) => {{
  const {{ hashValue, action }} = data || {{}};
  const el = document.querySelector('[{HASH_ATTR}="'+hashValue+'"]');
  if (!el) return {{status:'not_found'}};
  const t = action.type;
  try {{
    if (t === 'set_attribute') {{
      const kv = action.value || {{}};
      Object.entries(kv).forEach(([k,v]) => {{ if (v === null) el.removeAttribute(k); else el.setAttribute(k, v); }});
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
(data) => {{
  const {{ hashValue }} = data || {{}};
  const el = document.querySelector('[{HASH_ATTR}="'+hashValue+'"]');
  return el ? el.outerHTML : null;
}}"""
