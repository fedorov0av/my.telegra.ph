from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from typing import Annotated

from app import setup
from app.api.page import router_page
from app.utils.text_conversion import get_date_for_content
from app import setup
from .config import SqliteDB, PostgresDB, DATABASE_DIR


TITLE = 'Нужен url страницы'
SERVICE_NAME = 'FlashNote'
DESCRIPTION = 'Нужен url страницы'
PUBLISHED_TIME = '2024-10-25T13:22:57+0000'
MODIFIED_TIME = '2024-10-25T13:22:57+0000'
URL = 'https://flashnote.ph/Komu-podpischiki-DevOps-FMTema-sredovyj-dajdzhest--2-oktyabrya-prazdnuetsya-den-rozhdeniya-ehlektronnoj-pochty-10-25'
HTML_CONTENT = '<p><img src="https://files.catbox.moe/bl8kaz.jpg"/></p><pre>Нужен url страницы</pre>'


# Асинхронная функция, которую нужно запустить при старте
async def startup_task(app: FastAPI):
    # Ваши асинхронные операции (например, подключение к БД)
    database = SqliteDB()
    database.path = DATABASE_DIR / "app.db"
    
    session_maker = await setup.init_db(database)
    # Yield позволяет продолжить выполнение приложения
    yield

app = FastAPI(lifespan=startup_task, docs_url="/api/docs")
#DBSessionDep = Annotated[AsyncSession, Depends(setup.get_db_session)]

templates = Jinja2Templates(directory="app/templates")
app.mount("/static_js", StaticFiles(directory="app/templates/static/js"), name="static_js")
app.mount("/static_css", StaticFiles(directory="app/templates/static/css"), name="static_css")
app.mount("/static_images", StaticFiles(directory="app/templates/static/images"), name="static_images")

app.include_router(router_page)
setup.init_logging(setup.log.LogSettings())
logger.info(f"App start!")

# Указываем, чтобы эта функция запускалась при старте приложения

@app.get("/")
async def get_page(request: Request):
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

