from playwright.sync_api import Page
from pathlib import Path

from src.scraper.browser import create_browser
from src.scraper.paginator import (
    get_last_page,
    go_to_page,
)
from src.scraper.participant_parser import parse_participants
from src.storage.csv_writer import (
    save_participants,
    save_events
)
from src.scraper.event_parser import (
    select_event_filter,
    parse_events,
    select_distance,
    get_supported_distances
)
from src.scraper.waits import wait_for_results_table_ready
from src.utils import console


def main():

    RESULTS_URL = "https://heroleague.ru/results"

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    EVENTS_FILE = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "events.csv"
    )

    playwright, browser, page = create_browser()

    try:
        events = collect_events(page, RESULTS_URL)

        save_events(events, EVENTS_FILE)

        total_events = 0
        total_participants = 0


        for event in events:

            if event["city"] in {"ТУЛА"}:
                continue

            if not event["url"].startswith(
                "https://heroleague.ru/results"
            ):
                continue

            event_participants = collect_participants(page, event)
            total_participants += event_participants
            total_events += 1

    finally:
        browser.close()
        playwright.stop()

    print(f"\nВсего обработано мероприятий: {total_events}")
    print(f"\nВсего собрано участников: {total_participants}")


def collect_participants(
    page: Page,
    event: dict
) -> int:
    """
    Собирает участников мероприятия по всем выбранным дистанциям.

    Функция открывает страницу результатов мероприятия,
    последовательно переключает дистанции, проходит по всем
    страницам результатов и сохраняет найденных участников.

    Args:
        page (Page):
            Открытая страница браузера Playwright.

        event (dict):
            Словарь с информацией о мероприятии.
            Должен содержать:
                - event_id
                - name
                - city
                - url

        distances (list[str]):
            Список дистанций для сбора участников.
            Например:
                [
                    "1 km",
                    "5 km",
                    "10 km",
                    "21.1 km"
                ]

    Returns:
        int:
            Количество участников в данном мероприятии
    """
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    PARTICIPANTS_DIR = (
        PROJECT_ROOT
        / "data"
        / "raw"
    )

    page.goto(event["url"])

    console.event_started(event['name'], event['city'])

    page.wait_for_selector("[role='columnheader']")

    event_id = f"{event['event_id']}. {event['city']} {event['name']}"

    event_participants = 0

    distances = get_supported_distances(page)

    if not distances:
        console.distances_not_found(event["name"], event["city"])
        return event_participants


    for distance, site_distance in distances.items():

        console.distance_started(distance)

        if not select_distance(page, site_distance):
            console.distance_not_selected(distance)
            continue

        # ожидание загрузки кнопок пагинации на странице:
        wait_for_results_table_ready(page)
        page.wait_for_timeout(10_000)

        console.results_ready(distance)

        last_page = get_last_page(page)
        console.pages_detected(last_page)

        distance_participants = 0
        for page_num in range(1, last_page + 1):        # можно регулировать количетсво собираемых страниц участников

            console.page_progress(page_num, last_page)

            # переходим на нужную страницу
            go_to_page(page,page_num)

            # извлекаем участников
            participants = parse_participants(page, event['event_id'], distance)

            # считаем количество участников
            distance_participants += len(participants)

            # сохраняем в CSV
            save_participants(participants, event_id, PARTICIPANTS_DIR)

        console.end_progress()
        console.distance_finished(distance, distance_participants)
        event_participants += distance_participants

    console.event_finished(event['name'], event['city'], event_participants)

    return event_participants


def collect_events(
    page: Page,
    results_url: str
) -> list[dict]:
    """
    Собирает список мероприятий.

    Последовательность работы:
        1. Переходит на страницу результатов.
        2. Выбирает фильтр «Забег».
        3. Извлекает данные о мероприятиях.
        4. Добавляет уникальный event_id каждому мероприятию.
        5. Возвращает список мероприятий.

    Args:
        page (Page):
            Открытая страница Playwright.

        results_url (str):
            Ссылка на страницу результатов.

    Returns:
        list[dict]:
            Список мероприятий.
            Каждый элемент содержит данные мероприятия
            и уникальный event_id.
    """

    page.goto(results_url)

    page.wait_for_timeout(2000)

    select_event_filter(page)

    events = parse_events(page)

    # Добавляем id для каждого мероприятия
    for event_id, event in enumerate(events, start=1):
        event["event_id"] = event_id

    return events
