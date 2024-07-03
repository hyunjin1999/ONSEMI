from django.contrib import admin
from . import views
from django.urls import path, include

app_name = 'qa'
urlpatterns = [    
    path('chatting/', views.chatting, name='chatting'), 
    path('reset/', views.reset, name='reset'),    
]