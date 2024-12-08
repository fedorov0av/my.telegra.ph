from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.page import router_page


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static_js", StaticFiles(directory="app/templates/static/js"), name="static_js")
app.mount("/static_css", StaticFiles(directory="app/templates/static/css"), name="static_css")
app.mount("/static_images", StaticFiles(directory="app/templates/static/images"), name="static_images")

app.include_router(router_page)

@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="base.html"
    )