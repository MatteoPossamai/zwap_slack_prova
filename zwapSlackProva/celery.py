import os

from celery import Celery
from dotenv import load_dotenv

ENV_TYPE = 'local'
ENV_FILE_PATH = ".env"
load_dotenv(ENV_FILE_PATH)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zwapSlackProva.settings')

celery_app = Celery('zwapSlackProva')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
