import pytest
from src.file_handler import JSONFileHandler
from src.utils import save_vacancy_to_file


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
