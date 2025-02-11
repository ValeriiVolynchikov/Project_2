# src/file_handler.py

from abc import ABC, abstractmethod
import json
from typing import List, Dict


class FileHandler(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_vacancy(self, vacancy_data: dict) -> None:
        """Добавление вакансии в файл."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: int) -> None:
        """Удаление вакансии из файла."""
        pass

    @abstractmethod
    def filter_vacancies(self, filter_word: str) -> list:
        """Фильтрация вакансий по ключевым словам."""
        pass


class JSONFileHandler:
    """Класс для работы с JSON-файлами."""

    def __init__(self, filename: str = "data/vacancies.json") -> None:
        self._filename = filename

    def _load_data(self) -> List[Dict]:
        """
        Загружает данные из JSON-файла.
        :return: Список словарей с данными о вакансиях.
        """
        # try:
        #     with open(self._filename, "r", encoding="utf-8") as file:
        #         data = json.load(file)
        #         if not isinstance(data, list):  # Проверяем, что данные являются списком
        #             return []
        #         return data
        # except FileNotFoundError:
        #     return []  # Возвращаем пустой список, если файл не найден
        # except json.JSONDecodeError:
        #     print(f"Ошибка чтения файла {self._filename}: поврежденный JSON.")
        #     return []  # Возвращаем пустой список, если JSON поврежден
        """Загрузка данных из JSON-файла."""
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def add_vacancy(self, vacancy_data: Dict) -> None:
        """
        Добавляет вакансию в JSON-файл.
        :param vacancy_data: Словарь с данными о вакансии.
        """
        data = self._load_data()
        if vacancy_data not in data:  # Проверяем отсутствие дублей
            data.append(vacancy_data)
            self._save_data(data)
            print(f"Вакансия {vacancy_data['title']} успешно добавлена.")

    def delete_vacancy(self, vacancy_id: int) -> None:
        """
        Удаляет вакансию из JSON-файла по ID.
        :param vacancy_id: ID вакансии для удаления.
        """
        data = self._load_data()
        filtered_data = [v for v in data if v.get("id") != vacancy_id]
        if len(filtered_data) < len(data):
            print(f"Вакансия с ID {vacancy_id} успешно удалена.")
        self._save_data(filtered_data)

    def filter_vacancies(self, filter_words: list) -> List:
        """
        Фильтрует вакансии по ключевому слову в описании.
        :param filter_word: Ключевое слово для фильтрации.
        :return: Список словарей с отфильтрованными вакансиями.
        """
        data = self._load_data()
        if not data:
            return []

        return [
            v for v in data if isinstance(v, dict) and any(
                word.lower() in v.get("description", "").lower() for word in filter_words
            )
        ]
    def _save_data(self, data: List[Dict]) -> None:
        """
        Сохраняет данные в JSON-файл.
        :param data: Список словарей с данными о вакансиях.
        """
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
