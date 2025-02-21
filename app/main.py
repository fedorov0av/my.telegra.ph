from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from loguru import logger

from app import setup
from app.api.page import router_page
from app.api.seo import router_seo
from app.api.main_page import router_main_page
from .config.consts import config


DEV = config["DEV"]

if DEV:
    app = FastAPI(docs_url="/api/docs", redoc_url=None, exception_handlers=setup.exception_handlers)
else:
    app = FastAPI(docs_url=None, redoc_url=None, exception_handlers=setup.exception_handlers)

add_pagination(app)
app.mount("/static_js", StaticFiles(directory="app/templates/static/js"), name="static_js")
app.mount("/static_css", StaticFiles(directory="app/templates/static/css"), name="static_css")
app.mount("/static_images", StaticFiles(directory="app/templates/static/images"), name="static_images")

app.include_router(router_main_page)
app.include_router(router_seo)
app.include_router(router_page)

setup.init_logging(setup.log.LogSettings())
logger.info(f"App start!")