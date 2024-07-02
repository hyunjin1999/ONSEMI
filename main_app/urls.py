from django.contrib import admin
from . import views
from django.urls import path, include

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('introduce/', views.introduce, name='introduce'),
    path('family/', views.family, name='family'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('terms/',views.terms,name='terms')
]