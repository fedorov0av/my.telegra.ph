import re
from datetime import datetime
from transliterate import translit


def convert_text_for_url(text: str) -> str:
    # Заменяем пробелы на дефисы и убираем символы, которые не являются буквами или цифрами (кроме пробелов)
    text = re.sub(r'[^\w\s-]', '', text)  # Удаляем все символы, которые не буквы и не цифры
    text = text.replace(" ", "-")  # Заменяем пробелы на дефисы

    # Преобразуем кириллицу в латиницу
    text = translit(text, 'ru', reversed=True)
    text = re.sub(r'[^\w\s-]', '', text)  # снова очищаем строку от всех символов, которые не буквы и не цифры, т.к. к примеру мягкий знак после translit становиться "верхней запятой"

    return text.lower()

def get_date_for_content(date: str) -> str: #  date = '2024-10-25T13:22:57+0000'
    T_Z = '+0000'
    if isinstance(date, datetime):
        date = date.strftime('%Y-%m-%dT%H:%M:%S%z')
    if date[-5:] != T_Z:
        date += T_Z
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime("%B %d, %Y") # 'October 25, 2024'