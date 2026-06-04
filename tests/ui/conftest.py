import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def playwright_browser():
    print("PLAYWRIGHT FIXTURE LOADED")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )
        yield browser
        browser.close()

@pytest.fixture
def playwright_context(playwright_browser):
    context = playwright_browser.new_context(viewport={"width": 1280, "height": 800})
    yield context
    context.close()

@pytest.fixture
def page(playwright_context):
    page = playwright_context.new_page()
    yield page
    page.close()
