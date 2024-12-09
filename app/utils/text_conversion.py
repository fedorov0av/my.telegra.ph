import re
from transliterate import translit

def convert_text_for_url(text: str) -> str:
    # Заменяем пробелы на дефисы и убираем символы, которые не являются буквами или цифрами (кроме пробелов)
    text = re.sub(r'[^\w\s-]', '', text)  # Удаляем все символы, которые не буквы и не цифры
    text = text.replace(" ", "-")  # Заменяем пробелы на дефисы

    # Преобразуем кириллицу в латиницу
    text = translit(text, 'ru', reversed=True)
    text = re.sub(r'[^\w\s-]', '', text)  # снова очищаем строку от всех символов, которые не буквы и не цифры, т.к. к примеру мягкий знак после translit становиться "верхней запятой"

    return text.lower()