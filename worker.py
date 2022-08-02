import os

from celery import Celery

from database import SessionLocal
from etl import ETL
from models.postal_code import PostalCode

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")


def run_all_without_timezone():
    with SessionLocal() as session:
        postal_codes = session.query(PostalCode).filter(PostalCode.timezone.is_(None)).all()
        for postal_code in postal_codes:
            get_timezone.apply_async(args=[postal_code.index])
    return True


@celery.task(name='get_timezone')
def get_timezone(postal_code: str):
    timezone_title = ETL(postal_code).get_timezone_title()
    return timezone_title
