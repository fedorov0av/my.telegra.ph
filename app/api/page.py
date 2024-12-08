from typing import Union
from fastapi import APIRouter

from app.schemas.page import Item

router_page = APIRouter()


@router_page.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@router_page.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}