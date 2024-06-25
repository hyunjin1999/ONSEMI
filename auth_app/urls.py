from django.contrib import admin
from django.urls import path, include
from .views import auth_views

urlpatterns = [
    path("login/", auth_views.login_user),
    path("register/", auth_views.register_user),
    path("logout/", auth_views.login_user),
]
