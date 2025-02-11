from celery import Celery

from .config.consts import config
from .utils.seo import sync_add_index

celery = Celery(__name__)
celery.conf.broker_url = config["REDIS_URL"]

@celery.task()
def celery_add_index(page_url: str) -> None:
    sync_add_index(page_url)