import re
from bs4 import BeautifulSoup
from fastapi.templating import Jinja2Templates


def truncate_html_with_tags(content: str, max_length: int) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    plain_text = soup.get_text()
    truncated_text = plain_text[:max_length]
    last_space_pos = truncated_text.rfind(' ')
    if last_space_pos == -1:
        last_space_pos = max_length
    truncated_html = content[:len(plain_text[:last_space_pos])]
    truncated_soup = BeautifulSoup(truncated_html, 'html.parser')
    closed_html = str(truncated_soup)
    return closed_html

templates = Jinja2Templates(directory="app/templates")
templates.env.filters['truncate_html_with_tags'] = truncate_html_with_tags

