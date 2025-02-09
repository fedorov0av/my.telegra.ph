from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from loguru import logger

from ..config.consts import INDEXNOW_KEY

router_seo = APIRouter()

if INDEXNOW_KEY:
    @router_seo.get(f"/{INDEXNOW_KEY}.txt", response_class=PlainTextResponse) 
    async def get_key_txt():
        return INDEXNOW_KEY