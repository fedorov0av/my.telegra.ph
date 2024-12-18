from pydantic import BaseModel, Field

class PageS(BaseModel):
    page_title: str = Field(..., max_length=300)
    page_description: str = Field(..., max_length=300)
    page_path: str = Field(..., max_length=300)
    page_content: str = Field(..., max_length=6000)