import pytest
from src.api_handler import HeadHunterAPI
from src.file_handler import JSONFileHandler
from src.vacancy import Vacancy
from src.helpers import clean_html
from main import filter_vacancies_by_salary, display_vacancies, user_interaction


@pytest.fixture
def hh_api():
    """Фикстура для создания экземпляра HeadHunterAPI."""
    return HeadHunterAPI()


@pytest.fixture
def json_saver(tmp_path):
    """Фикстура для создания временного JSON-файла."""
    filename = tmp_path / "vacancies.json"
    saver = JSONFileHandler(filename=str(filename))
    return saver

#
# # Тестирование парсинга диапазона зарплат
# def test_parse_salary_range():
#     """Тестирует функцию parse_salary_range."""
#     # Корректный диапазон
#     result = parse_salary_range("100000-200000")
#     assert result == (100000.0, 200000.0)
#
#     # Некорректный формат
#     result = parse_salary_range("abc-def")
#     assert result == (0, float('inf'))
#
#     # Отсутствие разделителя
#     result = parse_salary_range("100000")
#     assert result == (0, float('inf'))
#
#     # Диапазон с отрицательными числами
#     result = parse_salary_range("-50000-150000")
#     assert result == (0, float('inf'))  # Теперь ожидаем (0, inf) вместо (-50000.0, 150000.0)


# Тестирование фильтрации вакансий по зарплате
def test_filter_vacancies_by_salary(json_saver):
    """Тестирует функцию filter_vacancies_by_salary."""
    # Добавляем тестовые вакансии в файл
    test_vacancies = [
        {"title": "Python Developer", "link": "http://example.com/python", "salary": 150000.0, "description": "Опыт работы с Python"},
        {"title": "Data Scientist", "link": "http://example.com/data", "salary": 200000.0, "description": "Знание машинного обучения"},
        {"title": "Junior Developer", "link": "http://example.com/junior", "salary": "Зарплата не указана", "description": "Без опыта работы"},
        {"title": "Backend Developer", "link": "http://example.com/backend", "salary": 180000.0, "description": "Опыт работы с Django"}
    ]
    for vacancy in test_vacancies:
        json_saver.add_vacancy(vacancy)

    # Фильтрация по диапазону зарплат
    filtered = filter_vacancies_by_salary(test_vacancies, (140000.0, 190000.0))
    assert len(filtered) == 2  # Ожидаем две вакансии в диапазоне
    assert all(140000.0 <= v["salary"] <= 190000.0 for v in filtered if isinstance(v["salary"], (int, float)))

    # Фильтрация без результата
    filtered = filter_vacancies_by_salary(test_vacancies, (300000.0, 400000.0))
    assert len(filtered) == 0  # Ожидаем пустой список


# Тестирование очистки HTML-тегов
def test_clean_html():
    """Тестирует функцию clean_html."""
    # Примеры с HTML-тегами
    assert clean_html("<highlighttext>Python</highlighttext>") == "Python"
    assert clean_html("<b>Senior</b> <i>QA</i> Engineer") == "Senior QA Engineer"
    assert clean_html("Опыт работы с <highlighttext>Python</highlighttext> и SQL") == "Опыт работы с Python и SQL"

    # Примеры без HTML-тегов
    assert clean_html("Программист Python") == "Программист Python"
    assert clean_html("") == "Описание отсутствует"
    assert clean_html(None) == "Описание отсутствует"


# Тестирование вывода вакансий
def test_display_vacancies(capsys):
    """Тестирует функцию display_vacancies."""
    test_vacancies = [
        {"title": "Python Developer", "link": "http://example.com/python", "salary": 150000.0, "description": "Опыт работы с Python"},
        {"title": "Data Scientist", "link": "http://example.com/data", "salary": "Зарплата не указана", "description": "Знание машинного обучения"}
    ]

    display_vacancies(test_vacancies)
    captured = capsys.readouterr()

    expected_output = (
        "Название: Python Developer\n"
        "Ссылка: http://example.com/python\n"
        "Зарплата: 150000.0 руб.\n"
        "Описание: Опыт работы с Python\n"
        "----------------------------------------\n"
        "Название: Data Scientist\n"
        "Ссылка: http://example.com/data\n"
        "Зарплата: Зарплата не указана руб.\n"
        "Описание: Знание машинного обучения\n"
        "----------------------------------------\n"
    )
    assert captured.out.strip() == expected_output.strip()


# Тестирование получения вакансий через API
def test_get_vacancies(hh_api):
    """Тестирует метод get_vacancies класса HeadHunterAPI."""
    vacancies = hh_api.get_vacancies("Python")
    assert isinstance(vacancies, list)
    assert len(vacancies) > 0
    for vacancy in vacancies:
        assert "title" in vacancy
        assert "link" in vacancy
        assert "salary" in vacancy
        assert "description" in vacancy


# Тестирование сохранения вакансий в файл
def test_save_vacancies(json_saver):
    """Тестирует метод add_vacancy класса JSONFileHandler."""
    test_vacancy = {
        "title": "Test Vacancy",
        "link": "http://example.com/test",
        "salary": 120000.0,
        "description": "Тестовое описание"
    }
    json_saver.add_vacancy(test_vacancy)

    data = json_saver._load_data()
    assert len(data) == 1
    saved_vacancy = data[0]
    assert saved_vacancy["title"] == "Test Vacancy"
    assert saved_vacancy["link"] == "http://example.com/test"
    assert saved_vacancy["salary"] == 120000.0
    assert saved_vacancy["description"] == "Тестовое описание"


# Тестирование фильтрации вакансий по ключевым словам
def test_filter_vacancies(json_saver):
    """Тестирует метод filter_vacancies класса JSONFileHandler."""
    test_vacancies = [
        {"title": "Python Developer", "link": "http://example.com/python", "salary": 150000.0, "description": "Опыт работы с Python"},
        {"title": "Data Scientist", "link": "http://example.com/data", "salary": 200000.0, "description": "Знание машинного обучения"},
        {"title": "Junior Developer", "link": "http://example.com/junior", "salary": "Зарплата не указана", "description": "Без опыта работы"},
        {"title": "Backend Developer", "link": "http://example.com/backend", "salary": 180000.0, "description": "Опыт работы с Django"}
    ]
    for vacancy in test_vacancies:
        json_saver.add_vacancy(vacancy)

    # Фильтрация по ключевому слову
    filtered = json_saver.filter_vacancies(["Python"])
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Python Developer"

    # Фильтрация без совпадений
    filtered = json_saver.filter_vacancies(["Java"])
    assert len(filtered) == 0

    # Пустой фильтр (возвращаем все вакансии)
    filtered = json_saver.filter_vacancies([])
    assert len(filtered) == len(test_vacancies)  # Теперь должно быть 4


# Тестирование обработки ошибок при взаимодействии с пользователем
def test_empty_search_query(monkeypatch, capsys):
    """Тестирует реакцию программы на пустой поисковый запрос."""
    monkeypatch.setattr("builtins.input", lambda _: "")  # Имитируем пустой ввод
    monkeypatch.setattr(HeadHunterAPI, "get_vacancies", lambda self, query: [])
    monkeypatch.setattr(JSONFileHandler, "filter_vacancies", lambda self, words: [])

    user_interaction()
    captured = capsys.readouterr()

    assert "Поисковый запрос не может быть пустым." in captured.out


def test_invalid_top_n_value(monkeypatch, capsys):
    """Тестирует реакцию программы на некорректное значение топ N."""
    inputs = iter(["Python", "abc", ""])  # Первый ввод — корректный запрос, второй — некорректное значение топ N
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(HeadHunterAPI, "get_vacancies", lambda self, query: [])
    monkeypatch.setattr(JSONFileHandler, "filter_vacancies", lambda self, words: [])

    user_interaction()
    captured = capsys.readouterr()

    assert "Некорректное значение для топ N. Ожидается положительное целое число." in captured.out


def test_no_vacancies_found(monkeypatch, capsys):
    """Тестирует случай, когда вакансий не найдено."""
    inputs = iter(["Python", "10", "", ""])  # Запрос, значение топ N и два пустых ввода для фильтрации и диапазона зарплат
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))  # Имитация ввода
    monkeypatch.setattr(HeadHunterAPI, "get_vacancies", lambda self, query: [])  # Возвращает пустой список вакансий
    monkeypatch.setattr(JSONFileHandler, "filter_vacancies", lambda self, words: [])  # Возвращает пустой список после фильтрации

    user_interaction()
    captured = capsys.readouterr()

    assert "По вашему запросу вакансий не найдено." in captured.out