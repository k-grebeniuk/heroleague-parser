import csv
from pathlib import Path


def save_participants(
    participants: list[dict],
    event_id: str,
    participants_dir: Path,
) -> None:
    """
    Сохраняет результаты участников мероприятия в CSV-файл.

    Файл сохраняется в указанную директорию и получает имя,
    сформированное на основе идентификатора мероприятия.

    Если файл уже существует, новые данные добавляются в конец файла.

    Args:
        participants (list[dict]):
            Список участников, полученный парсером.

        event_id (str):
            Идентификатор мероприятия, используемый для имени файла.

        participants_dir (Path):
            Директория для сохранения файлов участников.

    Returns:
        None:
            Функция сохраняет данные в файл и ничего не возвращает.
    """

    if not participants:
        print("Нет данных для сохранения.")
        return

    participants_dir.mkdir(parents=True, exist_ok=True,)

    file_path = participants_dir / f"{event_id}.csv"
    file_exists = file_path.exists()
    fieldnames = participants[0].keys()

    with open(file_path, "a", newline="", encoding="utf-8-sig",) as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames,)

        if not file_exists:
            writer.writeheader()

        writer.writerows(participants)



def save_events(
    events: list[dict],
    file_path: Path,
) -> None:
    """
    Сохраняет информацию о мероприятиях в CSV-файл.

    Если директория для сохранения отсутствует, она создаётся автоматически.
    Существующий файл перезаписывается актуальным набором данных.

    Args:
        events (list[dict]):
            Список мероприятий для сохранения.

        file_path (Path):
            Полный путь к файлу сохранения.

    Returns:
        None:
            Функция сохраняет данные в файл и ничего не возвращает.
    """

    if not events:
        print("Нет данных для сохранения.")
        return

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_exists = file_path.exists()
    fieldnames = events[0].keys()

    with file_path.open("w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(events)


