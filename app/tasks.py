from celery import Celery

from .config.consts import config
from .utils.seo import sync_add_index

app = Celery('worker')
app.conf.broker_url = config["REDIS_URL"]

@app.task
def add_index(page_url: str) -> None:
    sync_add_index(page_url)