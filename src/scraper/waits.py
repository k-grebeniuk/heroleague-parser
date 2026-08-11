from playwright.sync_api import Page


def wait_for_results_table_ready(page: Page) -> None:
    """
    Ожидает появления таблицы результатов после переключения дистанции.

    Функция используется после выбора новой дистанции перед началом
    парсинга участников. Она проверяет, что страница обновилась и
    таблица результатов имеет ожидаемую структуру:
    присутствует заголовок с колонкой "Фамилия" и загружено
    достаточное количество строк участников.

    Ожидание не гарантирует полную загрузку всех страниц результатов,
    а только подтверждает готовность текущей страницы к обработке.

    Args:
        page (Page):
            Открытая страница результатов Playwright.

    Returns:
        None:
            Функция завершает выполнение после успешного появления
            таблицы результатов или вызывает исключение при таймауте.
    """
    
    page.wait_for_function(
        """
        () => {

            const headers = [
                ...document.querySelectorAll("[role='columnheader']")
            ];

            const hasHeader = headers.some(
                header => header.innerText.includes("Фамилия")
            );

            const rows = document.querySelectorAll(
                "[role='row']"
            );

            return hasHeader && rows.length > 5;
        }
        """
    )