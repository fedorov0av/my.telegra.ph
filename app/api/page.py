from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates

from ..setup import DBSessionDep
from app.schemas.page import PageS
from ..db.models.page import Page
from ..utils.text_conversion import get_date_for_content, convert_text_for_url
from ..config.consts import SERVICE_NAME

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
async def get_page(session: DBSessionDep, url: str, request: Request):
    page_db: Page = await Page.get_page_by_url(session, url)
    if not page_db: 
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse(
        request=request, name="base.html",
        context={
            "title_tag": page_db.page_title + ' – ' + SERVICE_NAME,
            "title": page_db.page_title,
            "service_name": SERVICE_NAME,
            "description": page_db.page_description,
            "published_time": page_db.created_at,
            "modified_time": page_db.updated_at,
            "url": page_db.page_url,
            "date": get_date_for_content(page_db.created_at),
            "html_content": page_db.page_content,
            }
    )