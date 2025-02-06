from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse
from ..config.consts import SERVICE_NAME, INDEXNOW_KEY

templates = Jinja2Templates(directory="app/templates")
router_others = APIRouter()

if INDEXNOW_KEY:
    @router_others.get(f"/{INDEXNOW_KEY}.txt", response_class=PlainTextResponse) 
    async def get_key_txt():

        return INDEXNOW_KEY
    
@router_others.get("/")
async def get_robots_txt(request: Request,):
    return templates.TemplateResponse(
        request=request, name="base.html",
        context={
            "title_tag": SERVICE_NAME,
            "title": SERVICE_NAME,
            "service_name": SERVICE_NAME,
            "description": SERVICE_NAME,
            "published_time": SERVICE_NAME,
            "modified_time": SERVICE_NAME,
            "url": SERVICE_NAME,
            "date": SERVICE_NAME,
            "html_content": SERVICE_NAME,
            })