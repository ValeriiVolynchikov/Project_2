import pytest
from src.helpers import clean_html


def test_clean_html():
    """Тестирует функцию clean_html."""
    # Примеры с HTML-тегами
    assert clean_html("<highlighttext>Python</highlighttext>") == "Python"
    assert clean_html("<b>Senior</b> <i>QA</i> Engineer") == "Senior QA Engineer"
    assert clean_html("Опыт работы с <highlighttext>Python</highlighttext> и SQL") == "Опыт работы с Python и SQL"

    # Примеры без HTML-тегов
    assert clean_html("Программист Python") == "Программист Python"

    # Проверка пустой строки
    assert clean_html("") == "Описание отсутствует"  # Ожидаемое поведение для пустой строки
