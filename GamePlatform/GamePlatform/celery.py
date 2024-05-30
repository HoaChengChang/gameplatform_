import os
from celery import Celery
from gameApp.tasks import work_chain
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GamePlatform.settings')

app = Celery('GamePlatform')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# # 在 Celery 启动时立即执行一次任务
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(crontab(hour=0, minute=0, day_of_week=1), work_chain.s(), name='start_task_initially')