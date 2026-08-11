from pathlib import Path
import ast


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = PROJECT_ROOT / "docs" / "project_structure.md"


def get_functions(file_path: Path) -> list[tuple[str, str]]:
    """
    Извлекает список функций верхнего уровня из Python-файла.

    Функция анализирует исходный код с помощью AST,
    находит все функции верхнего уровня и получает
    их краткое описание из первой строки docstring.

    Args:
        file_path (Path):
            Путь к Python-файлу.

    Returns:
        list[tuple[str, str]]:
            Список кортежей вида:
                (
                    имя_функции,
                    краткое_описание
                )

            Если у функции отсутствует docstring,
            используется строка "Без описания".
    """

    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    functions = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):

            docstring = ast.get_docstring(node)

            if docstring:
                description = docstring.splitlines()[0]
            else:
                description = "Без описания"

            functions.append((node.name, description))

    return functions


def generate_project_structure() -> None:
    """
    Генерирует Markdown-документацию со структурой проекта.

    Функция проходит по всем Python-файлам в проекте,
    извлекает список функций верхнего уровня и их описания из docstring,
    после чего сохраняет полученную структуру в Markdown-файл.

    Последовательность работы:
        1. Создает директорию для выходного файла.
        2. Открывает файл документации для записи.
        3. Находит все Python-файлы проекта.
        4. Получает список функций каждого файла.
        5. Записывает структуру проекта в формате Markdown.
        6. Выводит сообщение о завершении генерации.

    Returns:
        None:
            Функция сохраняет документацию в файл и ничего не возвращает.
    """
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        file.write("# Структура проекта RUNNING-INSIGHTS\n")

        for file_path in sorted(PROJECT_ROOT.rglob("*.py")):

            functions = get_functions(file_path)

            file.write(f"\n---\n## `{file_path.relative_to(PROJECT_ROOT)}`\n")

            if not functions:
                file.write("&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**\n")
                continue

            #file.write("| Функция | Назначение |\n")
            #file.write("|----------|------------|\n")

            for func_name, description in functions:
                file.write(
                    f"&nbsp;&nbsp;&nbsp;&nbsp;**{func_name}()** | {description} <br>\n"
                )


    print(f"Документация сохранена в {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_project_structure()