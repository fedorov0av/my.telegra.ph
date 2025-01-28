from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from ..config.consts import INDEXNOW_KEY

router_others = APIRouter()

if INDEXNOW_KEY:
    @router_others.get(f"/{INDEXNOW_KEY}.txt", response_class=PlainTextResponse) 
    async def get_key_txt():
        return INDEXNOW_KEY