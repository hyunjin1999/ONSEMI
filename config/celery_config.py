from celery import Celery
import os
from django.conf import settings
from django.apps import apps

# Django settings module 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Django settings로부터 설정을 로드
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django 앱에서 작업 자동 검색
app.autodiscover_tasks(['orders_app', 'config'])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')