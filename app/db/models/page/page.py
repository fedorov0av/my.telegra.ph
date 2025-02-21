from __future__ import annotations

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession

from ..base import TimestampMixin
from ..base.declarative import Base


class PageDB(Base, TimestampMixin):
    __tablename__ = "page"
    id: Mapped[int] = mapped_column(primary_key=True)
    page_title: Mapped[str] = mapped_column(String(300))
    page_description: Mapped[str] = mapped_column(String(300))
    page_path: Mapped[str] = mapped_column(String(300))
    page_content: Mapped[str] = mapped_column(String(6096), nullable=True)
    page_url: Mapped[str] = mapped_column(String(300))
    
    
    @staticmethod
    async def add_page(session: AsyncSession, page_title: str, page_description: str, page_path: str,
                       page_content: str, page_url: str,) -> PageDB:
        page = PageDB(page_title=page_title, page_description=page_description, page_path=page_path,
                     page_content=page_content, page_url=page_url,)
        session.add(page)
        await session.commit()
        return page
    
    @staticmethod
    async def get_page_by_url(session: AsyncSession, page_url: str) -> PageDB | None:
        page_db = await PageDB.get_or_none(session, page_url=page_url)
        return page_db
    

    @staticmethod
    async def get_all_pages(session: AsyncSession) -> list[PageDB]:
        query = select(PageDB).order_by(PageDB.id)
        result = await session.scalars(query)
        pages_db = result.all()
        return pages_db