import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_sync.settings")

app = Celery("ecommerce_sync")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
