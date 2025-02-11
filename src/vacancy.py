# src/vacancy.py

class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = ["_title", "_link", "_salary", "_description"]

    def __init__(self, title: str, link: str, salary: float | str, description: str) -> None:
        self._title = self._validate_title(title)
        self._link = self._validate_link(link)
        self._salary = self._validate_salary(salary)
        self._description = self._validate_description(description)

    @staticmethod
    def _validate_title(title: str) -> str:
        """Приватный метод валидации названия вакансии."""
        if not title:
            raise ValueError("Название вакансии не может быть пустым.")
        return title

    @staticmethod
    def _validate_link(link: str) -> str:
        """Приватный метод валидации ссылки на вакансию."""
        if not link.startswith("http"):
            raise ValueError("Некорректная ссылка.")
        return link

    @staticmethod
    def _validate_salary(salary: str) -> float:
        """Приватный метод валидации зарплаты."""
        if salary is None or isinstance(salary, str) and salary.lower() == "зарплата не указана":
            return "Зарплата не указана"
        if isinstance(salary, (int, float)):
            return float(salary)
        try:
            # Попытка преобразования строки в число
            return float(salary.split("-")[0].replace(" ", "").replace("руб.", ""))
        except AttributeError:
            return "Зарплата не указана"
        except ValueError:
            return "Зарплата не указана"

    @staticmethod
    def _validate_description(description: str) -> str:
        """Приватный метод валидации описания вакансии."""
        if not description:
            return "Описание отсутствует."
        return description

    def to_dict(self) -> dict:
        """
        Преобразует объект Vacancy в словарь.
        :return: Словарь с данными о вакансии.
        """
        return {
            "title": self._title,
            "link": self._link,
            "salary": self._salary,
            "description": self._description
        }

    @property
    def title(self) -> str:
        return self._title

    @property
    def salary(self) -> float:
        return self._salary

    def __repr__(self) -> str:
        return f"Vacancy(title={self._title!r}, link={self._link!r}, salary={self._salary}, description={self._description!r})"

    def __lt__(self, other: 'Vacancy') -> bool:
        return self._salary < other.salary

    def __gt__(self, other: 'Vacancy') -> bool:
        return self._salary > other.salary
