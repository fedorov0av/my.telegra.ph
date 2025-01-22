from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from ..config.consts import config

api_key_header = APIKeyHeader(name="API-Key")

API_KEY = config["API_KEY"]

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key