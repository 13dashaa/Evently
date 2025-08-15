import os

from celery import Celery

from eventservice.config import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventservice.settings")

app = Celery("eventservice", broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
