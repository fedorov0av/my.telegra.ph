from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, Response
from loguru import logger

from ..db.models.page import PageDB
from ..config.consts import INDEXNOW_KEY
from ..setup import DBSessionDep

router_seo = APIRouter(tags=["Seo"])

if INDEXNOW_KEY:
    @router_seo.get(f"/{INDEXNOW_KEY}.txt", response_class=PlainTextResponse) 
    async def get_key_txt():
        return INDEXNOW_KEY

@router_seo.get(f'/robot.txt', response_class=PlainTextResponse)
async def get_robot_txt():
    data = """User-agent: *\nAllow: /\nCrawl-delay: 10"""
    return data

@router_seo.get(f'/sitemap.xml')
async def get_robot_txt(session: DBSessionDep):
    my_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
                <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
    pages = await PageDB.get_all_pages(session)
    urls = []
    for page in pages:
        urls.append(f"""<url>
              <loc>{page.page_url}</loc>
              <lastmod>{page.updated_at}</lastmod>
              <changefreq>weekly</changefreq>
              <priority>0.8</priority>
          </url>""")
    my_sitemap += "\n".join(urls)
    my_sitemap += """</urlset>"""
    return Response(content=my_sitemap, media_type="application/xml")