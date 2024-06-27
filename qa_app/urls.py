from django.contrib import admin
from . import views
from django.urls import path, include

app_name = 'qa'
urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('chating/', views.chating, name='chating'), 
    path('new_chat/', views.new_chat, name='new_chat'),
    path('reset/', views.reset, name='reset'),
    
]