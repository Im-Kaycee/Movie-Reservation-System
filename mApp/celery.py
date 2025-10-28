from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mApp.settings')

app = Celery('mApp')

# Load config from settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in all installed apps
app.autodiscover_tasks()
