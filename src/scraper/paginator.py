from playwright.sync_api import Page


def get_last_page(page: Page) -> int:
    """
    Определяет номер последней страницы пагинации.

    Args:
        page (Page):
            Открытая страница результатов Playwright.

    Returns:
        int:
            Номер последней страницы.
    """

    links = page.locator("nav[aria-label='Countries Pagination'] a").all_inner_texts()
    pages = [int(x) for x in links if x.isdigit()]
    

    if not pages:
        return 1

    return max(pages)


def go_to_page(page: Page, page_num: int) -> bool:
    """
    Переходит на указанную страницу пагинации.

    Если нужная страница не отображается,
    переключает окно пагинации кнопкой Next.

    Args:
        page (Page):
            Открытая страница Playwright.

        page_num (int):
            Номер страницы.

    Returns:
        bool:
            True - переход успешен.
            False - перейти не удалось.
    """

    # print(f"Переходим на страницу {page_num}")

    button = page.get_by_role("link", name=str(page_num), exact=True)

    while button.count() == 0:

        next_button = page.get_by_role("link",name="Next")

        if next_button.count() == 0:
            return False

        print(f"Страница {page_num} не видна, нажимаем Next")

        next_button.click()

        page.wait_for_timeout(300)

        button = page.get_by_role("link", name=str(page_num), exact=True)

    button.click()

    page.wait_for_timeout(1000)

    return get_current_page(page) == page_num


def get_current_page(page: Page) -> str:
    """
    Получает номер текущей активной страницы пагинации.
    Args:
        page (Page):
            Открытая страница Playwright.

    Returns:
        str:
            Номер активной страницы.
    """

    active_page = page.locator(
        "nav[aria-label='Countries Pagination'] [class*='_pageItemActive_']"
    ).inner_text()

    return active_page