from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from loguru import logger
from html_utils import nodes_to_html

from ..setup import DBSessionDep
from ..schemas.page import PageS, PageList, PageResponse
from ..secure import get_api_key
from ..db.models.page import Page
from ..utils.text_conversion import get_date_for_content, convert_text_for_url, get_date_for_title
from ..config.consts import SERVICE_NAME
from ..tasks import add_index

templates = Jinja2Templates(directory="app/templates")
router_page = APIRouter()


@router_page.post("/createPage/", response_model=PageResponse)
async def create_page(session: DBSessionDep, page: PageS, request: Request, api_key: str = Depends(get_api_key)) -> dict:
    """
    Creates a new page based on the request data.

    - page_title (str): The updated title of the page (max length: 300 characters).
    - page_description (str): The updated description of the page (max length: 300 characters).
    - page_path (str): The updated path for the page, used to generate the URL (max length: 300 characters).
    - page_url (Optional[str]): The updated URL for the page, can be left empty if not updating (max length: 300 characters).
    - page_content (List[Any]): The updated content of the page, typically a list of HTML nodes or text (max length: 10000 characters).
    - api_key: API key for authorization check.

    Returns:
        - Response with the result of the page creation.
    """
    page_path = convert_text_for_url(page.page_path) # Convert the page path to a URL-friendly format
    page_content_html = nodes_to_html(page.page_content)
    formatted_date = '-' + get_date_for_title() # Add the current date to the page path
    page_url = f"{str(request.base_url)}{page_path}{formatted_date}"
    check_page_db = await Page.get_page_by_url(session, page_url)
    if check_page_db:
        raise HTTPException(status_code=400, detail="Page with this url already exists")
    page_db: Page = await Page.add_page(
                    session = session,
                    page_title = f"{page.page_title}{formatted_date}",
                    page_description = f"{page.page_description}",
                    page_path = f"{page_path}{formatted_date}",
                    page_content = page_content_html,
                    page_url = page_url
                    )
    page_db = await Page.get_page_by_url(session, page_url)
    page.page_title = page_db.page_title
    page.page_description = page_db.page_description
    page.page_path = page_db.page_path
    page.page_content = page_db.page_content
    page.page_url = page_db.page_url
    add_index.delay(page_url)
    return {"ok": True, "result": page}

@router_page.put("/editPage/")
async def edit_page(session: DBSessionDep, page: PageS, request: Request, api_key: str = Depends(get_api_key)) -> PageS:
    """
    Updates an existing page in the database.

    - page_title (str): The updated title of the page (max length: 300 characters).
    - page_description (str): The updated description of the page (max length: 300 characters).
    - page_path (str): The updated path for the page, used to generate the URL (max length: 300 characters).
    - page_url (Optional[str]): The updated URL for the page, can be left empty if not updating (max length: 300 characters).
    - page_content (List[Any]): The updated content of the page, typically a list of HTML nodes or text (max length: 10000 characters).
    - api_key: API key for authorization check.

    Returns:
        - The updated page data.
    
    In case of error:
        - 404 if the page is not found.
        - 500 if the update fails.
    """
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
    page.page_url = page_url
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update page") from e
    return page

@router_page.get("/{page_path}")
async def get_page(session: DBSessionDep, page_path: str, request: Request):
    """
    Returns:
        - The HTML page with data from the database.
    
    In case of error:
        - 404 if the page is not found.
    """
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

@router_page.get("/getPageList/") 
async def get_page_list(session: DBSessionDep, request: Request, api_key: str = Depends(get_api_key)) -> PageList:
    """
    Retrieves a list of all pages in the system.

    - api_key: API key for authorization check.

    Returns:
        - A list of all pages with their titles and URLs.
    """
    pages_db: list[Page] = await Page.get_all_pages(session)
    page_list = PageList(page_list=[])
    for page_db in pages_db:
        page_list.page_list.append({
            "page_title": page_db.page_title,
            "page_url": page_db.page_url
        })
    return page_list
