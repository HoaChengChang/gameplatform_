import os
from celery import Celery
'''
加celery為了，使用crontab，定時去爬5大平台，相關設定在setting
'''

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GamePlatform.settings')

app = Celery('GamePlatform')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


