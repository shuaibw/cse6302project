from playwright.async_api import Page
from .js_snippets import HASH_JS

async def instrument_dom(page: Page):
    """Inject hashing + helper functions into the page.
    Safe to call multiple times; it is idempotent."""
    await page.add_init_script(HASH_JS)
    try:
        await page.evaluate(HASH_JS)
    except Exception:
        pass
