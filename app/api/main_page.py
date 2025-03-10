from fastapi import APIRouter, Request, Depends
from fastapi_pagination import Page, Params, set_params, set_page
from fastapi_pagination.ext.sqlalchemy import paginate
from loguru import logger
from typing import Any
from html_utils import nodes_to_html
from sqlalchemy import select

from app.secure import get_api_key
from app.db.models.page import PageDB
from app.schemas.page import PageContent, PageResponseMainS, PageMainS, PageOut
from app.config.consts import SERVICE_NAME
from app.setup import DBSessionDep
from app.utils.seo import add_index
from app.utils.jinja import templates

router_main_page = APIRouter(tags=["Main page"])

@router_main_page.post("/setMainPage/", response_model=PageResponseMainS)
async def set_main_page(session: DBSessionDep, page_content: PageContent, request: Request, api_key: str = Depends(get_api_key)):
    """
    Create or update a main page in the database.

    - page_content (List[Any]): The updated content of the page, typically a list of HTML nodes or text (max length: 10000 characters).
    - api_key: API key for authorization check.

    Returns:
        - The updated page data.
    """
    page_content_html = nodes_to_html(page_content.page_content)
    page_url = str(request.base_url)
    page_db: PageDB = await PageDB.get_page_by_url(session, page_url)
    if not page_db:
        page_db: PageDB = await PageDB.add_page(
                        session = session,
                        page_title = f"{SERVICE_NAME}",
                        page_description = f"{SERVICE_NAME}",
                        page_path = f"{SERVICE_NAME}",
                        page_media = page_content.page_media,
                        page_content = page_content_html,
                        page_url = page_url
                        )
        page_db: PageDB = await PageDB.get_page_by_url(session, page_url)
        await add_index(page_url)
    else:
        page_db.page_content = page_content_html
        session.add(page_db)
        await session.commit()
        page_db: PageDB = await PageDB.get_page_by_url(session, page_url)
    page = PageMainS(page_title=page_db.page_title, page_description=page_db.page_description, page_path=page_db.page_path, page_url=page_db.page_url, page_content=page_db.page_content)
    return {"ok": True, "result": page}

@router_main_page.get("/")
async def get_main_page(session: DBSessionDep, request: Request, page: int = 1, size: int = 4):
    """
    Returns:
        - The HTML main page.
    
    In case of error:
        - Return default page if the main page is not found.
    """
    set_page(Page[PageDB])
    set_params(Params(page=page, size=size))
    result: Page[PageDB] = await paginate(session, select(PageDB).order_by(PageDB.id.desc()), subquery_count=False)
    last_page: PageDB = await PageDB.get_last_page(session)
    logger.info(result.items)
    page_image = last_page.page_media
    page_cont = last_page.page_content
    page_url = last_page.page_url
    return templates.TemplateResponse(
        request=request, name="main_page/index.html",
        context={
            "title_tag": SERVICE_NAME,
            "title": SERVICE_NAME,
            "service_name": SERVICE_NAME,
            "description": SERVICE_NAME,
            "published_time": last_page.created_at,
            "modified_time": last_page.updated_at,
            "max_length": 250,
            "last_page": last_page,
            "otherPosts": result.items,
            "pages": {
                "total": result.total,
                "page": result.page,
                "size": result.size,
                "pages": result.pages
            }
            })

@router_main_page.get("/pages", response_model=Page[PageOut])
async def get_pages(session: DBSessionDep) -> Any:
    result = await paginate(session, select(PageDB).order_by(PageDB.id))
    return  result