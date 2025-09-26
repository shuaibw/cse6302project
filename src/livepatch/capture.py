import json
from pathlib import Path
from typing import Dict, Any
from playwright.async_api import Page, TimeoutError as PWTimeoutError

from .constants import HASH_ATTR

async def safe_wait(page: Page, wait_for: str, settle_ms: int):
    try:
        await page.wait_for_load_state(wait_for, timeout=30000)
    except PWTimeoutError:
        pass
    await page.wait_for_timeout(settle_ms)

async def capture_accessibility(page: Page):
    try:
        return await page.accessibility.snapshot(interesting_only=False)
    except Exception:
        return None

async def screenshot_multi(page: Page, out_dir: Path, viewports: Dict[str, Dict[str, Any]]):
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
