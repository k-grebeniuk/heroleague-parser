from playwright.sync_api import (
    sync_playwright,
    Playwright,
    Browser,
    Page
)


def create_browser() -> tuple[Playwright, Browser, Page]:
    """
    Создает экземпляр браузера Chromium.
    
    Returns:
        tuple:
            Playwright:
                Управление Playwright.

            Browser:
                Запущенный экземпляр браузера Chromium.

            Page:
                Открытая страница браузера.
    """

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    return playwright, browser, page