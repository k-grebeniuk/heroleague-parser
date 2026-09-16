# Структура проекта RUNNING-INSIGHTS

---
## `run.py`
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## `src\scraper\__init__.py`
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## `src\scraper\browser.py`
&nbsp;&nbsp;&nbsp;&nbsp;**create_browser()** | Создает экземпляр браузера Chromium. <br>

---
## `src\scraper\distances.py`
&nbsp;&nbsp;&nbsp;&nbsp;**is_supported_distance()** | Проверяет, используется ли дистанция в анализе. <br>

---
## `src\scraper\event_parser.py`
&nbsp;&nbsp;&nbsp;&nbsp;**select_event_filter()** | Выбирает фильтр "Забег" в списке мероприятий. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**parse_events()** | Извлекает список мероприятий со страницы результатов. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**normalize_url()** | Преобразует относительные ссылки в абсолютные. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**select_distance()** | Выбирает дистанцию в фильтре результатов мероприятия. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**normalize_distance()** | Приводит название дистанции к единому виду. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**get_supported_distances()** | Извлекает доступные дистанции мероприятия <br>

---
## `src\scraper\main.py`
&nbsp;&nbsp;&nbsp;&nbsp;**main()** | Без описания <br>
&nbsp;&nbsp;&nbsp;&nbsp;**collect_participants()** | Собирает участников мероприятия по всем выбранным дистанциям. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**collect_events()** | Собирает список мероприятий. <br>

---
## `src\scraper\paginator.py`
&nbsp;&nbsp;&nbsp;&nbsp;**get_last_page()** | Определяет номер последней страницы пагинации. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**go_to_page()** | Переходит на указанную страницу пагинации. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**get_current_page()** | Получает номер текущей активной страницы пагинации. <br>

---
## `src\scraper\participant_parser.py`
&nbsp;&nbsp;&nbsp;&nbsp;**get_headers()** | Извлекает названия колонок таблицы участников. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**parse_rows()** | Извлекает данные участников из строк таблицы. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**parse_participants()** | Полностью извлекает участников из таблицы результатов <br>

---
## `src\scraper\waits.py`
&nbsp;&nbsp;&nbsp;&nbsp;**wait_for_results_table_ready()** | Ожидает появления таблицы результатов после переключения дистанции. <br>

---
## `src\storage\__init__.py`
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## `src\storage\csv_writer.py`
&nbsp;&nbsp;&nbsp;&nbsp;**save_participants()** | Сохраняет результаты участников мероприятия в CSV-файл. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**save_events()** | Сохраняет информацию о мероприятиях в CSV-файл. <br>

---
## `src\tools\project_structure_generator.py`
&nbsp;&nbsp;&nbsp;&nbsp;**get_functions()** | Извлекает список функций верхнего уровня из Python-файла. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**generate_project_structure()** | Генерирует Markdown-документацию со структурой проекта. <br>

---
## `src\utils\__init__.py`
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## `src\utils\console.py`
&nbsp;&nbsp;&nbsp;&nbsp;**event_started()** | Выводит информацию о начале сбора участников мероприятия. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**distances_not_found()** | Выводит сообщение об отсутствии доступных для анализа дистанций. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**distance_started()** | Отображает начало обработки конкретной дистанции. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**distance_not_selected()** | Выводит сообщение о невозможности выбора дистанции на странице. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**results_ready()** | Выводит сообщение о готовности страницы к обработке результатов. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**pages_detected()** | Выводит количество обнаруженных страниц результатов. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**page_progress()** | Обновляет строку прогресса при обработке страниц результатов. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**distance_finished()** | Выводит итог обработки отдельной дистанции. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**event_finished()** | Выводит итоговый результат обработки мероприятия. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**end_progress()** | Завершает строку динамического прогресса в терминале. <br>
