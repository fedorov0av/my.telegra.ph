from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from loguru import logger

from app import setup
from app.api.page import router_page
from app.api.seo import router_seo
from app.api.main_page import router_main_page
from .config.consts import config
from app.config.consts import SERVICE_NAME

DEV = config["DEV"]

async def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        request=request, name="404.html",
        context={"service_name": SERVICE_NAME,},
        status_code = 404,
    )

templates = Jinja2Templates(directory="app/templates")

exception_handlers = {
    404: not_found_error,
}
if DEV:
    app = FastAPI(docs_url="/api/docs", redoc_url=None, exception_handlers=exception_handlers)
else:
    app = FastAPI(docs_url=None, redoc_url=None, exception_handlers=exception_handlers)

app.mount("/static_js", StaticFiles(directory="app/templates/static/js"), name="static_js")
app.mount("/static_css", StaticFiles(directory="app/templates/static/css"), name="static_css")
app.mount("/static_images", StaticFiles(directory="app/templates/static/images"), name="static_images")

app.include_router(router_main_page)
app.include_router(router_seo)
app.include_router(router_page)

setup.init_logging(setup.log.LogSettings())
logger.info(f"App start!")

