# Set the default Django settings module for the 'celery' program.
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hi_itis.settings')

app = Celery('hi_itis')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every': {
        'task': 'base.tasks.hello',
        "schedule": timedelta(seconds=30),
    },
}