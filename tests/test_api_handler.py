# tests/test_api_handler.py

import pytest
from src.api_handler import HeadHunterAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


def test_get_vacancies(hh_api):
    """Тестирует метод get_vacancies()."""
    vacancies = hh_api.get_vacancies("Python")
    assert isinstance(vacancies, list)
    assert len(vacancies) > 0
    for vacancy in vacancies:
        assert "name" in vacancy
        assert "alternate_url" in vacancy
        assert "snippet" in vacancy


def test_get_vacancies_with_salary(hh_api):
    """Тестирует получение вакансий с корректной зарплатой."""
    vacancies = hh_api.get_vacancies("Python")
    assert isinstance(vacancies, list)
    for vacancy in vacancies:
        assert "title" in vacancy
        assert "link" in vacancy
        assert "salary" in vacancy
        assert "description" in vacancy
        if isinstance(vacancy["salary"], str):
            assert vacancy["salary"] == "Зарплата не указана"


def test_get_vacancies_without_salary(hh_api):
    """Тестирует получение вакансий без зарплаты."""
    vacancies = hh_api.get_vacancies("Junior Developer")
    for vacancy in vacancies:
        if vacancy["salary"] == "Зарплата не указана":
            assert isinstance(vacancy["salary"], str)
