from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from app.config.consts import SERVICE_NAME

templates = Jinja2Templates(directory="app/templates")

async def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        request=request, name="404.html",
        context={"service_name": SERVICE_NAME,},
        status_code = 404,
    )

exception_handlers = {
    404: not_found_error,
}