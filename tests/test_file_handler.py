import pytest
import json
from unittest.mock import mock_open, patch
from src.file_handler import JSONFileHandler


@pytest.fixture
def json_file_handler():
    return JSONFileHandler("test_vacancies.json")


def test_add_vacancy(json_file_handler):
    vacancy_data = {
        "id": 1,
        "title": "Python Developer",
        "link": "https://example.com",
        "salary": 100000,
        "description": "<b>Описание</b> вакансии"
    }

    mock_data = json.dumps([])  # Изначально файл пуст
    with patch("builtins.open", mock_open(read_data=mock_data)), \
            patch("src.file_handler.JSONFileHandler._save_data") as mock_save:
        json_file_handler.add_vacancy(vacancy_data)
        mock_save.assert_called_once()
        # Проверка, что данные были очищены
        assert vacancy_data["description"] == "Описание вакансии"


def test_delete_vacancy(json_file_handler):
    vacancy_data = {
        "id": 1,
        "title": "Python Developer",
        "link": "https://example.com",
        "salary": 100000,
        "description": "Описание вакансии"
    }

    mock_data = json.dumps([vacancy_data])  # В файле есть одна вакансия
    with patch("builtins.open", mock_open(read_data=mock_data)), \
            patch("src.file_handler.JSONFileHandler._save_data") as mock_save:
        json_file_handler.delete_vacancy(1)
        mock_save.assert_called_once()  # Убедитесь, что _save_data был вызван

        # Проверка, что _save_data был вызван с пустым списком
        mock_save.assert_called_once_with([])  # Ожидаем, что после удаления списка вакансий будет пустым


def test_filter_vacancies(json_file_handler):
    mock_data = json.dumps([
        {"id": 1, "title": "Python Developer", "description": "Описание Python"},
        {"id": 2, "title": "Java Developer", "description": "Описание Java"}
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        filtered_vacancies = json_file_handler.filter_vacancies(["Python"])
        assert len(filtered_vacancies) == 1
        assert filtered_vacancies[0]["title"] == "Python Developer"


def test_filter_vacancies_by_salary(json_file_handler):
    mock_data = json.dumps([
        {"id": 1, "title": "Python Developer", "salary": 100000},
        {"id": 2, "title": "Java Developer", "salary": 80000},
        {"id": 3, "title": "C++ Developer", "salary": 120000}
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        filtered_vacancies = json_file_handler.filter_vacancies_by_salary((90000, 130000))
        assert len(filtered_vacancies) == 2
        assert all(v["salary"] >= 90000 and v["salary"] <= 130000 for v in filtered_vacancies)


def test_load_data_empty_file(json_file_handler):
    with patch("builtins.open", mock_open(read_data='')):
        data = json_file_handler._load_data()
        assert data == []
