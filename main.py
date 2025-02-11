# # main.py
#
# from src.api_handler import HeadHunterAPI
# from src.file_handler import JSONFileHandler
# from src.vacancy import Vacancy
#
#
# def user_interaction():
#     """Функция для взаимодействия с пользователем через консоль."""
#     search_query = input("Введите поисковый запрос: ")
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words_input = input("Введите ключевые слова для фильтрации вакансий (через пробел): ")
#     filter_words = filter_words_input.split()  # Разбиваем ввод на список слов
#
#     hh_api = HeadHunterAPI()
#     json_saver = JSONFileHandler()
#
#     # Получаем вакансии с API
#     hh_vacancies = hh_api.get_vacancies(search_query)
#
#     # Преобразуем данные в список объектов Vacancy
#     vacancies_list = [
#         Vacancy(
#             title=vacancy.get("name", "Название не указано"),
#             link=vacancy.get("alternate_url", "Ссылка не указана"),
#             salary=vacancy.get("salary", {}).get("from", None) if vacancy.get("salary") else "Зарплата не указана",
#             description=vacancy.get("snippet", {}).get("requirement", "Описание отсутствует")
#         )
#         for vacancy in hh_vacancies
#     ]
#
#     # Сохраняем вакансии в JSON-файл
#     for vacancy in vacancies_list:
#         json_saver.add_vacancy(vacancy.to_dict())
#
#     # Фильтрация вакансий
#     filtered_vacancies = json_saver.filter_vacancies(filter_words)
#
#     # Сортировка и вывод результатов
#     sorted_vacancies = sorted(
#         filtered_vacancies,
#         key=lambda v: v["salary"] if isinstance(v["salary"], (int, float)) else 0,
#         reverse=True
#     )[:top_n]
#
#     if not sorted_vacancies:
#         print("По вашему запросу вакансий не найдено.")
#     else:
#         print(f"Топ {len(sorted_vacancies)} вакансий:")
#         for vacancy in sorted_vacancies:
#             print(f"Название: {vacancy['title']}\n"
#                   f"Ссылка: {vacancy['link']}\n"
#                   f"Зарплата: {vacancy['salary']} руб.\n"
#                   f"Описание: {vacancy['description']}\n"
#                   f"{'-' * 40}")
#
#
# if __name__ == "__main__":
#     user_interaction()
# main.py

from src.api_handler import HeadHunterAPI
from src.file_handler import JSONFileHandler
from src.vacancy import Vacancy
from src.helpers import clean_html


def display_vacancies(vacancies):
    for vacancy in vacancies:
        title = vacancy.get("title", "Без названия")
        link = vacancy.get("link", "Ссылка отсутствует")
        salary = vacancy.get("salary", "Зарплата не указана")
        description = clean_html(vacancy.get("description", "Описание отсутствует"))  # Очищаем описание

        print(f"Название: {title}")
        print(f"Ссылка: {link}")
        print(f"Зарплата: {salary} руб.")
        print(f"Описание: {description}")
        print("-" * 40)  # Разделитель


def user_interaction():
    """Функция для взаимодействия с пользователем через консоль."""
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words_input = input("Введите ключевые слова для фильтрации вакансий (через пробел): ")
    filter_words = filter_words_input.split()

    hh_api = HeadHunterAPI()
    json_saver = JSONFileHandler()

    # Получаем вакансии с API
    hh_vacancies = hh_api.get_vacancies(search_query)

    # Преобразуем данные в список объектов Vacancy
    vacancies_list = [
        Vacancy(
            title=vacancy["title"],
            link=vacancy["link"],
            salary=vacancy["salary"],
            description=vacancy["description"]
        )
        for vacancy in hh_vacancies
    ]

    # Сохраняем вакансии в файл
    for vacancy_data in hh_vacancies:
        json_saver.add_vacancy(vacancy_data)

    # Фильтрация вакансий
    filtered_vacancies = json_saver.filter_vacancies(filter_words)

    # Сортировка и вывод результатов
    sorted_vacancies = sorted(
        filtered_vacancies,
        key=lambda v: v["salary"] if isinstance(v["salary"], (int, float)) else 0,
        reverse=True
    )[:top_n]

    # if not sorted_vacancies:
    #     print("По вашему запросу вакансий не найдено.")
    # else:
    #     print(f"Топ {len(sorted_vacancies)} вакансий:")
    #     for vacancy in sorted_vacancies:
    #         print(f"Название: {vacancy['title']}\n"
    #               f"Ссылка: {vacancy['link']}\n"
    #               f"Зарплата: {vacancy['salary']} руб.\n"
    #               f"Описание: {vacancy['description']}\n"
    #               f"{'-' * 40}")
    if   not sorted_vacancies:
        print("По вашему запросу вакансий не найдено.")

    else:
        print(f"Топ {len(sorted_vacancies)} вакансий:")
        display_vacancies(sorted_vacancies)  # Вызов функции для отображения вакансий


if __name__ == "__main__":
    user_interaction()
