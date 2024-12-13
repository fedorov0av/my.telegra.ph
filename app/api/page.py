from typing import Union
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.schemas.page import Item
from ..utils.text_conversion import get_date_for_content
from ..config.consts import TITLE, SERVICE_NAME, DESCRIPTION, PUBLISHED_TIME, MODIFIED_TIME, \
                            URL, HTML_CONTENT

templates = Jinja2Templates(directory="app/templates")
router_page = APIRouter()

@router_page.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@router_page.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@router_page.get("/{url}")
async def get_page(url: str, request: Request):
    print(url)
    return templates.TemplateResponse(
        request=request, name="base.html",
        context={
            "title_tag": TITLE + ' – ' + SERVICE_NAME,
            "title": TITLE,
            "service_name": SERVICE_NAME,
            "description": DESCRIPTION,
            "published_time": PUBLISHED_TIME,
            "modified_time": MODIFIED_TIME,
            "url": URL,
            "date": get_date_for_content(PUBLISHED_TIME),
            "html_content": HTML_CONTENT,
            }
    )