from typing import Dict, Any, Optional
from playwright.async_api import Page
from .js_snippets import RESOLVE_ELEMENT_JS, APPLY_ACTION_JS, GET_OUTER_HTML_JS

async def resolve_element_hash(page: Page, locator: Dict[str, Any]) -> Optional[str]:
    strategy = locator.get('strategy', 'auto')
    value = locator.get('value')
    if not value:
        return None
    return await page.evaluate(RESOLVE_ELEMENT_JS, {"selector": value, "strategy": strategy})

async def apply_action(page: Page, hash_value: str, action: Dict[str, Any]) -> Dict[str, Any]:
    return await page.evaluate(APPLY_ACTION_JS, {"hashValue": hash_value, "action": action})

async def get_outer_html(page: Page, hash_value: str) -> Optional[str]:
    return await page.evaluate(GET_OUTER_HTML_JS, {"hashValue": hash_value})
