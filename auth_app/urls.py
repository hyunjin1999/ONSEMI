from django.contrib import admin
from django.urls import path, include
from .views import auth_views, profile_update_views, profile_views

urlpatterns = [
    path("login/", auth_views.login_user),
    path("register/", auth_views.register_user, name="ds"),
    path("logout/", auth_views.logout_user),
    path("profile/", profile_views.show_user_profile),
    path("profile/update/", profile_update_views.update_profile),
    path("profile/update/password/", profile_update_views.update_password),
]
