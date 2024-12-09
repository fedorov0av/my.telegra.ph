from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.page import router_page
from app.utils.text_conversion import get_date_for_content

TITLE = 'Нужен url страницы'
SERVICE_NAME = 'FlashNote'
DESCRIPTION = 'Нужен url страницы'
PUBLISHED_TIME = '2024-10-25T13:22:57+0000'
MODIFIED_TIME = '2024-10-25T13:22:57+0000'
URL = 'https://flashnote.ph/Komu-podpischiki-DevOps-FMTema-sredovyj-dajdzhest--2-oktyabrya-prazdnuetsya-den-rozhdeniya-ehlektronnoj-pochty-10-25'
HTML_CONTENT = '<p><img src="https://files.catbox.moe/bl8kaz.jpg"/></p><pre>Нужен url страницы</pre>'


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static_js", StaticFiles(directory="app/templates/static/js"), name="static_js")
app.mount("/static_css", StaticFiles(directory="app/templates/static/css"), name="static_css")
app.mount("/static_images", StaticFiles(directory="app/templates/static/images"), name="static_images")

app.include_router(router_page)


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