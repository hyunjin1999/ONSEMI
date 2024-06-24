from django.contrib import admin
from django.urls import path, include
from .views import post_views, upload_views

app_name = 'blog'

urlpatterns = [
    path("post", post_views.post_all),
    path("post/upload", upload_views.post_upload),
]