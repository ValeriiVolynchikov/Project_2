# src/helpers.py
import re

def clean_html(raw_html: str) -> str:
    """
    Удаляет HTML-теги из строки.
    :param raw_html: Строка с HTML-тегами.
    :return: Чистая строка без HTML-тегов.
    """
    if not raw_html:
        return "Описание отсутствует"
    clean_text = re.sub(r"<.*?>", "", raw_html)  # Удаляем все теги между <>
    return clean_text.strip()
