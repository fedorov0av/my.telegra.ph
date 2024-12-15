from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from ..setup import DBSessionDep
from app.schemas.page import PageS
from ..db.models.page import Page
from ..utils.text_conversion import get_date_for_content, convert_text_for_url
from ..config.consts import TITLE, SERVICE_NAME, DESCRIPTION, PUBLISHED_TIME, MODIFIED_TIME, \
                            URL, HTML_CONTENT

templates = Jinja2Templates(directory="app/templates")
router_page = APIRouter()

@router_page.post("/add_page/")
async def add_page(session: DBSessionDep, page: PageS):
    page_db = await Page.add_page(
                    session = session,
                    page_title = page.page_title,
                    page_description = page.page_description,
                    page_path = page.page_path,
                    page_content = page.page_content,
                    page_url = convert_text_for_url(page.page_path)
                    )
    return page

# @router_page.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}

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