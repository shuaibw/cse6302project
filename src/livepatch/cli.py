import argparse
import json
from .api import run_capture_with_patches

def _parse_patches_file(patches_file: str):
    import json, os
    if not os.path.exists(patches_file):
        raise FileNotFoundError(patches_file)
    data = json.loads(open(patches_file, 'r', encoding='utf-8').read())
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
