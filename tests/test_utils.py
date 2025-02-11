# tests/test_utils.py

import pytest
from src.file_handler import JSONFileHandler
from src.utils import save_vacancy_to_file
from src.utils import clean_html


@pytest.fixture
def json_saver(tmp_path):
    """Фикстура для создания временного JSON-файла."""
    filename = tmp_path / "vacancies.json"
    saver = JSONFileHandler(filename=str(filename))
    return saver


def test_save_vacancy_to_file(json_saver):
    """Тестирует функцию save_vacancy_to_file."""
    # Создаем тестовую вакансию
    test_vacancy = {
        "title": "Python Developer",
        "link": "https://example.com/python-dev",
        "salary": 100000,
        "description": "Требуется опыт работы с Python."
    }

    # Сохраняем вакансию в файл
    save_vacancy_to_file(test_vacancy, json_saver)

    # Проверяем, что вакансия успешно добавлена
    data = json_saver._load_data()
    assert len(data) == 1
    assert data[0]["title"] == "Python Developer"

    # Проверяем обработку некорректных данных
    with pytest.raises(ValueError):
        save_vacancy_to_file("Invalid Data", json_saver)


def test_clean_html():
    """Тестирует функцию clean_html."""
    # Примеры с HTML-тегами
    assert clean_html("<highlighttext>Python</highlighttext>") == "Python"
    assert clean_html("<b>Senior</b> <i>QA</i> Engineer") == "Senior QA Engineer"
    assert clean_html("Опыт работы с <highlighttext>Python</highlighttext> и SQL") == "Опыт работы с Python и SQL"

    # Примеры без HTML-тегов
    assert clean_html("Программист Python") == "Программист Python"
    assert clean_html("") == ""
    assert clean_html(" ") == ""

    # Примеры с неправильными тегами
    assert clean_html("<invalidtag>Python</invalidtag>") == "Python"
    assert clean_html("<<>>Python<<>>") == "Python"
