from playwright.sync_api import Page


def get_headers(page: Page) -> list[str]:
    """
    Извлекает названия колонок таблицы участников.

    Args:
        page (Page): Открытая страница браузера Playwright, содержащая таблицу результатов.
    Returns:
        list[str]: Список названий колонок таблицы.
                  Например:
                  [
                    "Номер",
                    "Имя",
                    "Фамилия",
                    "Категория"
                  ]
    """

    headers = page.locator("div[role='columnheader']").all_inner_texts()

    return [header.replace("↕", "").strip()for header in headers]


def parse_rows(page: Page, headers: list[str]) -> list[dict]:
    """
    Извлекает данные участников из строк таблицы.

    Args:
        page (Page): Открытая страница результатов Playwright.
        headers (list[str]): Список названий колонок таблицы.
    Returns:
        list[dict]: Список словарей, где каждый словарь представляет одного участника.
    """

    results = []
    rows = page.locator("div[role='row']").all()

    for row in rows:
        cells = row.locator("div[role='cell']").all_inner_texts()

        if not cells:
            continue

        participant = {}

        for header, value in zip(headers, cells):
            participant[header] = value

        results.append(participant)

    return results


def parse_participants(
    page: Page,
    event_id: str,
    distance: str
) -> list[dict]:
    """
    Полностью извлекает участников из таблицы результатов
    и добавляет информацию о мероприятии.

    Args:
        page (Page):
            Открытая страница результатов Playwright.

        event_id (int):
            Идентификатор мероприятия.

        distance (str):
            Дистанция забега.

    Returns:
        list[dict]:
            Список участников соревнования.
    """

    headers = get_headers(page)
    participants = parse_rows(page, headers)

    for participant in participants:
        participant["event_id"] = event_id
        participant["distance"] = distance

    return participants