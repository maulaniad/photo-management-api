import os

from celery import Celery
from tasks.scheduler import BEAT_SCHEDULE


os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")

app = Celery("App")

app.autodiscover_tasks()
app.config_from_object('django.conf:settings', namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.conf.beat_schedule = BEAT_SCHEDULE
