# urls.py
from django.urls import path
from . import views

app_name = 'voice_app'

urlpatterns = [
    path('', views.upload_audio, name='upload'),
    path('result/<int:voice_id>/', views.result, name='result'),
]