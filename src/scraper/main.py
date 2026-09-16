
from pathlib import Path

from src.scraper.browser import create_browser
from src.storage.csv_writer import (
    save_events
)
from src.scraper.collector import (
    collect_events,
    collect_participants
)


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

