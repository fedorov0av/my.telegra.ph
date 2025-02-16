from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from loguru import logger
from html_utils import nodes_to_html

from ..secure import get_api_key
from ..db.models.page import Page
from ..schemas.page import PageContent, PageResponseMainS, PageMainS
from ..config.consts import SERVICE_NAME, HTML_MAIN_PAGE_CONT_NOT_FOUND
from ..setup import DBSessionDep
from ..utils.seo import add_index


router_main_page = APIRouter()
templates = Jinja2Templates(directory="app/templates")

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
    logger.info(f"Set main page : {page_url}")
    page_db: Page = await Page.get_page_by_url(session, page_url)
    logger.info(f"page_db : {page_db}")

    if not page_db:
        page_db: Page = await Page.add_page(
                        session = session,
                        page_title = f"{SERVICE_NAME}",
                        page_description = f"{SERVICE_NAME}",
                        page_path = f"{SERVICE_NAME}",
                        page_content = page_content_html,
                        page_url = page_url
                        )
        page_db: Page = await Page.get_page_by_url(session, page_url)
        await add_index(page_url)
    else:
        page_db.page_content = page_content_html
        session.add(page_db)
        await session.commit()
        page_db: Page = await Page.get_page_by_url(session, page_url)
    page = PageMainS(page_title=page_db.page_title, page_description=page_db.page_description, page_path=page_db.page_path, page_url=page_db.page_url, page_content=page_db.page_content)
    return {"ok": True, "result": page}

@router_main_page.get("/")
async def get_main_page(session: DBSessionDep, request: Request,):
    """
    Returns:
        - The HTML main page.
    
    In case of error:
        - Return default page if the main page is not found.
    """
    pages: list[Page] = await Page.get_all_pages(session)
    print(pages[-1])
    page = await Page.get_page_by_url(session, str(request.base_url))
    return templates.TemplateResponse(
        request=request, name="main_page.html",
        context={
            "title_tag": SERVICE_NAME,
            "title": SERVICE_NAME,
            "service_name": SERVICE_NAME,
            "description": SERVICE_NAME,
            "published_time": SERVICE_NAME,
            "modified_time": SERVICE_NAME,
            "url": SERVICE_NAME,
            "date": SERVICE_NAME,
            "topPost": pages[-1].page_content if pages[-1] else 'No content',
            })