from abc import ABC, abstractmethod
import requests
from src.vacancy import Vacancy
from src.helpers import clean_html
from typing import List, Dict, Any
from typing import cast


# class APIHandler(ABC):
#     """Абстрактный класс для работы с API платформ с вакансиями."""
#
#     @abstractmethod
#     def connect(self, url: str, params: dict) -> dict:
#         """Метод для подключения к API."""
#         pass
#
#     @abstractmethod
#     def get_vacancies(self, keyword: str) -> List[Dict]:
#         """Метод для получения вакансий."""
#         pass
#
#
# class HeadHunterAPI(APIHandler):
#     """Класс для работы с API HeadHunter."""
#
#     _BASE_URL = "https://api.hh.ru/vacancies"
#
#     def connect(self, url: str, params: dict) -> Dict[str, Any]:
#         """Подключение к API HeadHunter."""
#         response = requests.get(url, params=params)
#         if response.status_code != 200:
#             raise ConnectionError(f"Ошибка подключения к API: {response.status_code}")
#         return response.json()  # Убедитесь, что ответ - это словарь
class APIHandler(ABC):
    """Абстрактный класс для работы с API платформ с вакансиями."""

    @abstractmethod
    def connect(self, url: str, params: dict) -> Dict[str, Any]:
        """Метод для подключения к API."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Метод для получения вакансий."""
        pass


class HeadHunterAPI(APIHandler):
    """Класс для работы с API HeadHunter."""

    _BASE_URL = "https://api.hh.ru/vacancies"

    def connect(self, url: str, params: dict) -> Dict[str, Any]:
        """Подключение к API HeadHunter."""
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка подключения к API: {response.status_code}")

        # Явно указываем, что ответ является словарем
        return cast(Dict[str, Any], response.json())


    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получение вакансий с hh.ru по ключевому слову."""
        params = {"text": keyword, "per_page": 100}
        try:
            data = self.connect(self._BASE_URL, params)
            return [
                {
                    "title": item.get("name", "Название не указано"),
                    "link": item.get("alternate_url", "Ссылка не указана"),
                    "salary": item.get("salary", {}).get("from", None) if item.get("salary") else "Зарплата не указана",
                    "description": clean_html(item.get("snippet", {}).get("requirement", "Описание отсутствует"))
                }
                for item in data.get("items", [])
            ]

        except ConnectionError as e:
            print(f"Произошла ошибка: {e}")
            return []
