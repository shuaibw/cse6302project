# Live Patch Capture (Minimal Usage)

This directory contains the `livepatch` module for applying structured accessibility (or other) patches to a live webpage and capturing before/after artifacts.

## Features
- Multi-viewport screenshots (configurable in `livepatch/constants.py`).
- Deterministic element hashing and patch application.
- Before/after HTML and (optionally) accessibility snapshot capture.
- Per-patch before/after outer HTML slices and verification.
- Visual debug banner example (see `visual_debug_banner` patch in `sample_patch.json`).

## Sample Patch File
See `sample_patch.json` for examples of patch actions:
- set_attribute
- append_child
- replace_outer_html
- set_text

Each patch entry:
```
{
  "id": "unique_patch_id",
  "locator": { "strategy": "css" | "xpath" | "hash" | "auto", "value": "CSS_OR_XPATH_OR_HASH" },
  "action": { "type": "set_attribute" | "append_child" | ... , "value": <string|object> },
  "verify": { "must_contain": ["substring"], "must_not_contain": ["substring"] }
}
```

## Patch Entry Structure (Detailed)

Each patch object in `sample_patch.json` (and any patch file you provide) follows this schema:

```
{
  "id": "string (recommended)",
  "locator": {
    "strategy": "css" | "xpath" | "hash" | "auto",
    "value": "string"
  },
  "action": {
    "type": "set_attribute" | "remove_attribute" | "replace_inner_html" | "replace_outer_html" | "set_text" | "append_child" | "insert_before" | "insert_after",
    "value": <string | object | array | null>
  },
  "verify": {
    "must_contain": [ "substring", ... ],
    "must_not_contain": [ "substring", ... ]
  },
  "meta": { /* optional, reserved for tags, notes, etc. */ }
}
```

### Fields Explained

**id** (string): Unique, human-readable identifier. If omitted, an auto id like `patch_001` is generated. Used in manifest and file names (`<id>_before.html`).

**locator** (object): How to find exactly one DOM element before applying the action.
- strategy:
  - `css`: Interpret `value` as a CSS selector (must match exactly one element).
  - `xpath`: Interpret `value` as an XPath expression (must match exactly one element).
  - `hash`: Use a previously computed deterministic hash attribute on the element.
  - `auto`: Try CSS; if not unique, try interpreting as hash; then XPath.
- value: The selector / hash string.

**action** (object): Mutation to perform.
- type + value mapping:
  - `set_attribute`: value = object `{ attr: newValue, ... }` (set or update attributes; future enhancement may allow `null` to remove).
  - `remove_attribute`: value = string or array of attribute names to remove.
  - `replace_inner_html`: value = HTML string for `element.innerHTML`.
  - `replace_outer_html`: value = HTML string replacing the element itself (original hash may become stale).
  - `set_text`: value = plain text assigned to `textContent`.
  - `append_child`: value = HTML snippet; its parsed nodes are appended as children.
  - `insert_before`: value = HTML snippet inserted before the element.
  - `insert_after`: value = HTML snippet inserted immediately after the element.

**verify** (object, optional): Post-apply substring assertions against the element's (original-hash) outerHTML.
- `must_contain`: All must be present; otherwise `verify_status = fail_contains`.
- `must_not_contain`: None may be present; otherwise `verify_status = fail_not_contains`.
- If omitted, verification defaults to `ok` when action succeeds.

**meta** (object, optional): Reserved. Suggested future keys: `tags`, `notes`, `severity`.

### Manifest Output Per Patch
`manifest.json` includes for each patch:
- id
- locator (echoed)
- action_type
- status (`applied`, `not_found`, `error`, etc.)
- resolved_hash (pre-action hash of target element)
- apply_result (status + optional error message)
- verify_status (`ok`, `fail_contains`, `fail_not_contains`)

Artifacts written to `patches/`:
- `<id>_before.html` – Outer HTML before mutation.
- `<id>_after.html` – Outer HTML after mutation (if still resolvable by original hash; structural replacements may prevent capture until re-resolve logic is added).

### Best Practices
1. Use stable selectors (avoid brittle nth-child chains when possible).
2. Combine related attribute tweaks in one `set_attribute` action to minimize extra DOM hashing cost.
3. For large structural HTML injection, consider wrapping in a distinct container with an id to simplify follow-up patches.
4. When using `replace_outer_html`, plan subsequent patches to target the new structure with a fresh locator (hash changes).
5. Keep `verify` substrings minimal (e.g. match just `aria-label="Toggle navigation menu"` rather than entire HTML blocks).

### Example (Visual Banner)
```
{
  "id": "visual_debug_banner",
  "locator": { "strategy": "css", "value": "body" },
  "action": {
    "type": "append_child",
    "value": "<div id=\"a11y-visual-banner\" style=\"position:fixed;top:0;left:0;width:100%;background:#d32f2f;color:#fff;z-index:99999;padding:10px 16px;\">Accessibility Patch Applied</div>"
  },
  "verify": { "must_contain": ["a11y-visual-banner"] }
}
```

---

## Run Example
From inside `src` (so that Python resolves the package):
```bash
python -m livepatch --url https://cse.buet.ac.bd/web/ \
  --patches sample_patch.json \
  --out out/buet_test_run \
  --verbose
```
Output structure:
```
out/
  buet_test_run/
    before/
      desktop_hd.png
      mobile_modern.png
      page.html
      a11y.json (if enabled)
    after/
      desktop_hd.png
      mobile_modern.png
      page.html
      a11y.json (if enabled)
    patches/
      <patch_id>_before.html
      <patch_id>_after.html
    manifest.json
```

## Common Issues
- If a patch shows `not_found`, refine the locator or try `strategy: auto`.
- For structural changes (`replace_outer_html`), the original hash may change; future enhancement will re-resolve automatically.
- Use the `visual_debug_banner` patch to visually confirm after state in screenshots.

## Next Ideas (Not yet implemented)
- Locator ambiguity diagnostics (match counts).
- Visual diff (pixel comparison) and a11y delta reporting.
- Discovery mode to export candidate element hashes & selectors.
