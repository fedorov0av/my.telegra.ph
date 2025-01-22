from pydantic import BaseModel, Field, Json
from typing import List, Union, Any

class PageS(BaseModel):
    page_title: str = Field(..., max_length=300)
    page_description: str = Field(..., max_length=300)
    page_path: str = Field(..., max_length=300)
    page_url: str | None = Field(..., max_length=300)
    page_content: List[Any] = Field(..., max_length=10000)

class PageList(BaseModel):
    page_list: List[dict] = Field(..., max_length=10000) # '{"page_title": "page_url", ... }'