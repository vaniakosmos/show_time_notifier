from celery import Celery

from core import settings


app = Celery()
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks([
    'core.trakt',
])
