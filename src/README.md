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
