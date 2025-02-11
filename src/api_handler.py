# src/api_handler.py

from abc import ABC, abstractmethod
import requests


class APIHandler(ABC):
    """Абстрактный класс для работы с API платформ с вакансиями."""

    @abstractmethod
    def connect(self, url: str, params: dict) -> dict:
        """Метод для подключения к API."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list:
        """Метод для получения вакансий."""
        pass


class HeadHunterAPI(APIHandler):
    """Класс для работы с API HeadHunter."""

    _BASE_URL = "https://api.hh.ru/vacancies"

    def connect(self, url: str, params: dict) -> dict:
        """Подключение к API HeadHunter."""
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка подключения к API: {response.status_code}")
        return response.json()

    def get_vacancies(self, keyword: str) -> list:
        """Получение вакансий по ключевому слову."""
        params = {"text": keyword, "per_page": 100}
        try:
            data = self.connect(self._BASE_URL, params)
            return [item for item in data.get("items", []) if item is not None]
        except ConnectionError as e:
            print(f"Произошла ошибка: {e}")
            return []
