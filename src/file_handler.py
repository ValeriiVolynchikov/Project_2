from abc import ABC, abstractmethod
import json
from typing import List, Dict, Any
from src.helpers import clean_html


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

    def _load_data(self) -> list[dict[str, Any]]:
        """
        Загружает данные из JSON-файла.
        :return: Список словарей с данными о вакансиях.
        """
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                content = file.read()
                if not content:  # Проверка на пустой файл
                    return []
                return json.loads(content)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []  # Обработка ошибок декодирования JSON

    def add_vacancy(self, vacancy_data: Dict) -> None:
        """
        Добавляет вакансию в JSON-файл.
        :param vacancy_data: Словарь с данными о вакансии.
        """
        data = self._load_data()

        # Очищаем описание перед добавлением
        vacancy_data["description"] = clean_html(vacancy_data.get("description", ""))

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
            self._save_data(filtered_data)  # Сохраняем обновленный список

    def filter_vacancies(self, filter_words: List[str]) -> List[Dict]:
        """
        Фильтрует вакансии по ключевому слову в описании.
        :param filter_word: Ключевое слово для фильтрации.
        :return: Список словарей с отфильтрованными вакансиями.
        """
        data = self._load_data()
        if not data or not isinstance(data, list):
            return []

        # Если фильтр пуст, возвращаем все вакансии
        if not filter_words:
            return data

        return [
            v for v in data if isinstance(v, dict) and any(
                word.lower() in (
                    clean_html(v.get("description", "Описание отсутствует") or "Описание отсутствует")).lower()
                for word in filter_words
            )
        ]

    def filter_vacancies_by_salary(self, salary_range: tuple) -> List[Dict]:
        """
        Фильтрует вакансии по указанному диапазону зарплат.
        :param salary_range: Кортеж (min_salary, max_salary).
        :return: Список отфильтрованных вакансий.
        """
        data = self._load_data()
        min_salary, max_salary = salary_range
        return [
            v for v in data
            if isinstance(v["salary"], (int, float)) and min_salary <= v["salary"] <= max_salary
        ]


    def _save_data(self, data: List[Dict]) -> None:
        """
        Сохраняет данные в JSON-файл.
        :param data: Список словарей с данными о вакансиях.
        """
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
