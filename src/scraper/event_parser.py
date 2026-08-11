from playwright.sync_api import Page
from src.scraper.distances import is_supported_distance


def select_event_filter(page: Page) -> None:
    """
    Выбирает фильтр "Забег" в списке мероприятий.
    Args:
        page (Page):
            Открытая страница Playwright.
    Returns:
        None:
            Функция изменяет состояние страницы.
    """

    #открываем селектор - выпадающий список
    selector = page.locator(".select-activity-container .select-activity__control")
    selector.click()

    #выбираем "Забег"
    option = page.get_by_role("option", name="Забег", exact=True)
    option.wait_for()
    option.click()
    page.wait_for_timeout(3000)


def parse_events(page: Page) -> list[dict]:
    """
    Извлекает список мероприятий со страницы результатов.
    Args:
        page (Page):
            Открытая страница Playwright.
    Returns:
        list[dict]:
            Список мероприятий.
    """

    cards = page.locator("li._item_18tis_50")
    events = []

    for i in range(cards.count()):

        card = cards.nth(i)
        raw_url = card.locator("a").get_attribute("href")

        event = {
            "date": card.locator("span").first.inner_text(),
            "city": card.locator("b").inner_text(),
            "name": card.locator("p").inner_text(),
            "url": normalize_url(raw_url)
        }
        events.append(event)

    return events


def normalize_url(url: str | None) -> str | None:
    """
    Преобразует относительные ссылки в абсолютные.
    """

    if url is None:
        return None

    if url.startswith("/"):
        return f"https://heroleague.ru{url}"

    return url



def select_distance(page: Page, site_distance: str) -> bool:
    """
    Выбирает дистанцию в фильтре результатов мероприятия.

    Функция находит элемент фильтра по названию дистанции,
    отображаемому на сайте, и переключает таблицу результатов
    на выбранную дистанцию.

    Args:
        page (Page):
            Открытая страница результатов Playwright.

        site_distance (str):
            Название дистанции в формате сайта.
            Например:
                "5км"
                "10км"
                "21,1км"

    Returns:
        bool:
            True — дистанция успешно найдена и выбрана.

            False — фильтр с указанной дистанцией
            отсутствует на странице.
    """

    locator = page.locator(f"label[for='{site_distance}_filter']")

    if locator.count() == 0:
        return False

    locator.click()
    page.wait_for_timeout(300)

    return True


def normalize_distance(distance: str) -> str:
    """
    Приводит название дистанции к единому виду.

    Args:
        distance (str):
            Название дистанции с сайта.

    Returns:
        str:
            Нормализованное название дистанции.
    """

    distance = distance.lower()
    distance = distance.replace(",", ".")
    distance = distance.replace(" ", "")
    distance = distance.replace("km", "км")

    if distance == "21км":
        return "21.1 км"

    if distance == "21.1км":
        return "21.1 км"

    if distance == "1км":
        return "1 км"

    if distance == "5км":
        return "5 км"

    if distance == "10км":
        return "10 км"

    return distance



def get_supported_distances(page: Page) -> dict[str, str]:
    """
    Извлекает доступные дистанции мероприятия
    и оставляет только те, которые используются в анализе.

    Функция получает список дистанций со страницы мероприятия,
    нормализует их названия и фильтрует ненужные категории
    (например: эстафеты, детские дистанции, корпоративные забеги).

    Args:
        page (Page):
            Открытая страница результатов Playwright.

    Returns:
        dict[str, str]:
            Словарь поддерживаемых дистанций.
            Ключ:
                Нормализованное название дистанции.
            Значение:
                Название дистанции на сайте.
            Например:
                {
                    "5 км": "5 km",
                    "10 км": "10 km",
                    "21 км": "21.1 km"
                }
    """
    page.wait_for_selector("label[for$='_filter']")

    distances = {}

    labels = page.locator("label[for$='_filter']")
    labels.first.wait_for()

    for i in range(labels.count()):

        site_name = labels.nth(i).inner_text().strip()

        normalized_name  = normalize_distance(site_name)

        if not is_supported_distance(normalized_name ):
            continue

        distances[normalized_name ] = site_name

    return distances