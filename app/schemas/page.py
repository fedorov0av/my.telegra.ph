from pydantic import BaseModel, Field, Json

class PageS(BaseModel):
    page_title: str = Field(..., max_length=300)
    page_description: str = Field(..., max_length=300)
    page_path: str = Field(..., max_length=300)
    page_url: str | None = Field(..., max_length=300)
    page_content: Json = Field(..., max_length=6000)