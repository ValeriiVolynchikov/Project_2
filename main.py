from src.api_handler import HeadHunterAPI
from src.file_handler import JSONFileHandler
from src.helpers import clean_html, parse_salary_range
from src.vacancy import Vacancy


def display_vacancies(vacancies: list) -> None:
    """Отображает список вакансий."""
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


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем через консоль."""

    # Поисковый запрос (обязательный)
    search_query = input("Введите поисковый запрос: ").strip()
    if not search_query:
        print("Поисковый запрос не может быть пустым.")
        return

    # Количество вакансий (опционально, по умолчанию 10)
    top_n_input = input("Введите количество вакансий для вывода в топ N (по умолчанию 10): ").strip()
    top_n = 10  # Значение по умолчанию
    if top_n_input:
        if not top_n_input.isdigit() or int(top_n_input) <= 0:
            print("Некорректное значение для топ N. Ожидается положительное целое число.")
            return
        top_n = int(top_n_input)

    # Ключевые слова для фильтрации (опционально)
    filter_words_input = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").strip()
    filter_words = filter_words_input.split() if filter_words_input else []

    # Диапазон зарплат (опционально)
    salary_range_input = input("Введите диапазон зарплат (минимальная-максимальная): ").strip()
    salary_range = (0, float('inf'))  # По умолчанию, если пользователь не ввел диапазон
    if salary_range_input:
        salary_range = parse_salary_range(salary_range_input)
        if salary_range == (0, float('inf')):
            print("Некорректный формат диапазона зарплат. Используйте формат: минимум-максимум")
            return

    hh_api = HeadHunterAPI()
    json_saver = JSONFileHandler()

    # Получаем вакансии с API
    hh_vacancies = hh_api.get_vacancies(search_query)

    # Преобразуем данные в список объектов Vacancy
    vacancies_list = []
    for vacancy in hh_vacancies:
        salary = vacancy.get("salary")

        if salary is None:
            salary_value = "Зарплата не указана"
        elif isinstance(salary, dict):
            # Получаем значение из словаря, и если оно None, устанавливаем значение по умолчанию
            salary_value = str(salary.get("from")) if salary.get("from") is not None else "Зарплата не указана"
        else:
            salary_value = str(salary)

        # Убедимся, что salary_value - это строка
        if salary_value == "Зарплата не указана" or (isinstance(salary_value, str) and not salary_value.isdigit()):
            salary_value = "Зарплата не указана"

        # Создаем объект Vacancy и обрабатываем возможную ошибку
        try:
            vacancies_list.append(
                Vacancy(
                    title=vacancy["title"],
                    link=vacancy["link"],
                    salary=salary_value,  # salary_value всегда строка
                    description=vacancy["description"]
                ).to_dict()
            )
        except ValueError as e:
            print(f"Ошибка в вакансии '{vacancy['title']}': {e}")

    # Сохраняем вакансии в файл
    for vacancy_data in vacancies_list:
        json_saver.add_vacancy(vacancy_data)

    # Фильтрация и сортировка вакансий
    filtered_vacancies = json_saver.filter_vacancies(filter_words) if filter_words else vacancies_list
    ranged_vacancies = filter_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sorted(
        ranged_vacancies,
        key=lambda v: v["salary"] if isinstance(v["salary"], (int, float)) else 0,
        reverse=True
    )[:top_n]

    if not sorted_vacancies:
        print("По вашему запросу вакансий не найдено.")
    else:
        print(f"Топ {len(sorted_vacancies)} вакансий:")
        display_vacancies(sorted_vacancies)


def filter_vacancies_by_salary(vacancies: list, salary_range: tuple) -> list:
    """
    Фильтрует вакансии по указанному диапазону зарплат.
    :param vacancies: Список словарей с данными о вакансиях.
    :param salary_range: Кортеж (min_salary, max_salary).
    :return: Список отфильтрованных вакансий.
    """
    min_salary, max_salary = salary_range
    return [
        v for v in vacancies
        if isinstance(v["salary"], (int, float)) and min_salary <= v["salary"] <= max_salary
    ]


if __name__ == "__main__":
    user_interaction()
