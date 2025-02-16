import re
import drawsvg as draw
from datetime import datetime
from transliterate import translit
from ..config.consts import GOOGLE_FONTNAME_LOGO, PATH_LOGO_SVG

def convert_text_for_url(text: str) -> str:
    """
    Converts a string to a URL-friendly format.

    - Strips leading and trailing spaces.
    - Replaces spaces with hyphens.
    - Removes non-alphanumeric characters (except spaces).
    - Converts Cyrillic characters to Latin letters.
    - Removes any remaining non-alphanumeric characters after transliteration.

    Args:
        - text: The string to be converted.

    Returns:
        - The formatted string in lowercase.
    """
    text = text.strip()
    # Replace spaces with hyphens and remove characters that are not letters or digits (except spaces)
    text = re.sub(r'[^\w\s-]', '', text)  # Remove all characters that are not letters or digits
    text = text.replace(" ", "-")  # Replace spaces with hyphens
    # Convert Cyrillic characters to Latin characters
    text = translit(text, 'ru', reversed=True)
    text = re.sub(r'[^\w\s-]', '', text)  # Clean the string again from non-alphanumeric characters, as for example, the soft sign after transliteration becomes an apostrophe
    return text.lower()

def get_date_for_content(date: str) -> str:
    """
    Formats a datetime string for content display.

    - Ensures the date has the correct timezone information.
    - Returns the formatted date in the "Month day, Year" format (e.g., "October 25, 2024").

    Args:
        - date: The datetime string to be formatted (in ISO format, e.g., '2024-10-25T13:22:57+0000').

    Returns:
        - The formatted date as a string (e.g., "October 25, 2024").
    """
    T_Z = '+0000'
    if isinstance(date, datetime):
        date = date.strftime('%Y-%m-%dT%H:%M:%S%z')
    if date[-5:] != T_Z:
        date += T_Z
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime("%B %d, %Y")  # 'October 25, 2024'

def get_date_for_title() -> str:
    """
    Returns the current date formatted for the title.

    - Returns the current date in the format "MM-DD-YY" (e.g., "01-26-23").

    Returns:
        - The formatted date as a string (e.g., "01-26-23").
    """
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%m-%d-%y")
    return formatted_date

def save_logo_svg_from_text(text: str) -> draw.Drawing:
    """
    Converts text to a logo SVG image.

    - Converts the text into a drawing object using the drawsvg library.

    Args:
        - text: The text to be converted into a logo SVG image.

    Returns:
        - The drawing object representing the logo SVG image.
    """
    uppercase_count = sum(1 for c in text if c.isupper())
    lowercase_count = sum(1 for c in text if c.islower())
    width = lowercase_count * 16 + uppercase_count * 20
    height = 50
    d = draw.Drawing(width, height, origin='center')
    d.embed_google_font(GOOGLE_FONTNAME_LOGO, text=set(text))
    d.append(draw.Text(text, 35, 0, 0, center=True, font_family=GOOGLE_FONTNAME_LOGO))
    d.save_svg(PATH_LOGO_SVG)