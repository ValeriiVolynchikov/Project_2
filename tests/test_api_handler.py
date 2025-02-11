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
