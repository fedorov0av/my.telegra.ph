from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates

from ..setup import DBSessionDep
from app.schemas.page import PageS
from ..db.models.page import Page
from ..utils.text_conversion import get_date_for_content, convert_text_for_url
from ..config.consts import SERVICE_NAME
from loguru import logger
from html_utils import nodes_to_html, json_loads

templates = Jinja2Templates(directory="app/templates")
router_page = APIRouter()

@router_page.post("/createPage/") # добавление страницы
async def create_page(session: DBSessionDep, page: PageS, request: Request):
    page_path = convert_text_for_url(page.page_path)
    page_url = str(request.base_url) + page_path
    page_content_nodes = json_loads(page.page_content)
    page_content_html = nodes_to_html(page_content_nodes)
    page_db: Page = await Page.add_page(
                    session = session,
                    page_title = page.page_title,
                    page_description = page.page_description,
                    page_path = page_path,
                    page_content = page_content_html,
                    page_url = page_url
                    )
    page_db = await Page.get_page_by_url(session, page_url)
    page.page_title = page_db.page_title
    page.page_description = page_db.page_description
    page.page_path = page_db.page_path
    page.page_content = page_db.page_content
    page.page_url = page_db.page_url
    return page

@router_page.put("/editPage/") # обновление страницы
async def edit_page(session: DBSessionDep, page: PageS, request: Request):
    page_path = convert_text_for_url(page.page_path)
    page_url = str(request.base_url) + page_path
    page_db: Page = await Page.get_page_by_url(session, page_url)
    if not page_db:
        raise HTTPException(status_code=404, detail="Page not found")
    page_db.page_title = page.page_title
    page_db.page_description = page.page_description
    page_db.page_path = page.page_path
    page_db.page_content = page.page_content
    page_db.page_url = page_url
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update page") from e
    return page_db

@router_page.get("/{page_path}") # получение страницы
async def get_page(session: DBSessionDep, page_path: str, request: Request):
    page_url = str(request.base_url) + page_path
    page_db: Page = await Page.get_page_by_url(session, page_url)
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





#############
# @router_page.put("/getPage/") # обновление страницы
# async def update_page(session: DBSessionDep, page: PageS, request: Request):
#     page_path = convert_text_for_url(page.page_path)
#     page_url = str(request.base_url) + page_path
#     page_db: Page = await Page.get_page_by_url(session, page_url)
#     if not page_db:
#         raise HTTPException(status_code=404, detail="Page not found")
#     page_db.page_title = page.page_title
#     page_db.page_description = page.page_description
#     page_db.page_path = page.page_path
#     page_db.page_content = page.page_content
#     page_db.page_url = page_url
#     try:
#         await session.commit()
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail="Failed to update page") from e
#     return page_db
# @router_page.put("/getPageList/") # обновление страницы
# async def update_page(session: DBSessionDep, page: PageS, request: Request):
#     page_path = convert_text_for_url(page.page_path)
#     page_url = str(request.base_url) + page_path
#     page_db: Page = await Page.get_page_by_url(session, page_url)
#     if not page_db:
#         raise HTTPException(status_code=404, detail="Page not found")
#     page_db.page_title = page.page_title
#     page_db.page_description = page.page_description
#     page_db.page_path = page.page_path
#     page_db.page_content = page.page_content
#     page_db.page_url = page_url
#     try:
#         await session.commit()
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail="Failed to update page") from e
#     return page_db
# @router_page.put("/getViews/") # обновление страницы
# async def update_page(session: DBSessionDep, page: PageS, request: Request):
#     page_path = convert_text_for_url(page.page_path)
#     page_url = str(request.base_url) + page_path
#     page_db: Page = await Page.get_page_by_url(session, page_url)
#     if not page_db:
#         raise HTTPException(status_code=404, detail="Page not found")
#     page_db.page_title = page.page_title
#     page_db.page_description = page.page_description
#     page_db.page_path = page.page_path
#     page_db.page_content = page.page_content
#     page_db.page_url = page_url
#     try:
#         await session.commit()
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail="Failed to update page") from e
#     return page_db
