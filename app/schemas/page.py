from pydantic import BaseModel, Field
from typing import List, Any, Optional

class PageS(BaseModel):
    page_title: str = Field(..., max_length=300)
    page_description: str = Field(..., max_length=300)
    page_path: str = Field(..., max_length=300)
    page_url: str = Field(None, max_length=300)
    page_media: str = Field(..., max_length=300)
    page_content: List[Any] = Field(..., max_length=10000)

class PageMainS(PageS):
    page_content: str = Field(..., max_length=10000)

class PageResponse(BaseModel):
    ok: bool = Field(True)
    result: PageS

class PageResponseMainS(PageResponse):
    result: PageMainS

class PageList(BaseModel):
    page_list: List[dict] = Field(..., max_length=10000) # '{"page_title": "page_url", ... }'

class PageContent(BaseModel):
    page_media: str = Field(..., max_length=300)
    page_content: List[Any] = Field(..., max_length=10000)

class PageOut(PageS):
    page_content: str = Field(..., max_length=6096)