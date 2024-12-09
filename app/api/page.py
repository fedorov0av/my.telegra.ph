from typing import Union
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.schemas.page import Item
from ..utils.text_conversion import get_date_for_content

templates = Jinja2Templates(directory="app/templates")
router_page = APIRouter()

TITLE = 'Кому: подписчики DevOps FMТема: средовый дайджест 📩 2 октября празднуется день рождения электронной почты'
SERVICE_NAME = 'Telegraph'
DESCRIPTION = 'Кому: подписчики DevOps FMТема: средовый дайджест'
PUBLISHED_TIME = '2024-10-25T13:22:57+0000'
MODIFIED_TIME = '2024-10-25T13:22:57+0000'
URL = 'https://telegra.ph/Komu-podpischiki-DevOps-FMTema-sredovyj-dajdzhest--2-oktyabrya-prazdnuetsya-den-rozhdeniya-ehlektronnoj-pochty-10-25'
HTML_CONTENT = '<p><img src="https://files.catbox.moe/bl8kaz.jpg"/></p><pre>Кому: подписчики DevOps FM<br/>Тема: средовый дайджест </pre><br/><br/>📩 2 октября празднуется день рождения электронной почты. Именно в этот день в 1971 году инженер Рэй Томлинсон отправил первое в истории человечества сообщение по e-mail. Пс-с-с: у нас есть <a href="https://t.me/go_honey_money">своя рассылка</a>. <br/><br/>⚫️ <a href="https://t.me/go_honey_money">Зарелизили</a> новую стабильную ветку PostgreSQL 17.<br/><br/>Обновления для этой версии будут выходить в течение пяти лет, вплоть до ноября 2029 года. Из тех, что имеются сейчас: <br/><br/>• ускорили выполнение операции <code>VACUUM</code> и сократили потребление совместно используемых ресурсов благодаря новой структуре данных;<br/>• добавили утилиту <code>pg_createsubscriber</code>, которая преобразует физическую реплику в новую логическую;<br/>• обновили <code>pg_upgrade</code>: теперь она сохраняет слоты репликации как у издателей, так и у пользователей. <br/><br/>Посмотреть все нововведения можно <a href="https://t.me/go_honey_money">тут</a>. <br/><br/>Кстати, поддержка ветки PostgreSQL 12 будет прекращена 14 ноября.<br/><br/>🟡 Ещё один релиз — MongoDB 8.0. Благодаря архитектурным улучшениям эта версия работает более чем на 30% быстрее предыдущих. Ещё появились новые варианты использования зашифрованных данных. Подробности — <a href="https://t.me/go_honey_money">по ссылке</a>.<br/><br/>⚫️ На InfoQ <a href="https://t.me/go_honey_money">рассказали</a>, как минимизировать задержку и стоимость в распределённых системах. Если очень коротко: вам поможет маршрутизация с учётом зоны. <br/><br/>🟡 На Dev <a href="https://t.me/go_honey_money">разобрали</a> ротацию резервных копий с помощью <a href="https://t.me/go_honey_money">nxs-backup</a>.   <br/> <br/>#devops #PostgreSQL #MongoDB #nxsbackup<p><strong>100% рабочие сигналы <a href="https://t.me/go_honey_money" target="_blank">👑 ТУТ 👑</a>  либо через оператора </strong><a href="https://t.me/go_honey_money" target="_blank"><strong>@TEST</strong></a> ❤️</p>'

@router_page.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@router_page.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@router_page.get("/{url}")
async def get_page(url: str, request: Request):
    print(url)
    return templates.TemplateResponse(
        request=request, name="base.html",
        context={
            "title_tag": TITLE + ' – ' + SERVICE_NAME,
            "title": TITLE,
            "service_name": SERVICE_NAME,
            "description": DESCRIPTION,
            "published_time": PUBLISHED_TIME,
            "modified_time": MODIFIED_TIME,
            "url": URL,
            "date": get_date_for_content(PUBLISHED_TIME),
            "html_content": HTML_CONTENT,
            }
    )