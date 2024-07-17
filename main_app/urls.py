from . import views
from django.urls import path

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('introduce/', views.introduce, name='introduce'),
    path('family/', views.family, name='family'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('terms/',views.terms,name='terms'),
    path('user_page/',views.user_page, name='user_page'),
]