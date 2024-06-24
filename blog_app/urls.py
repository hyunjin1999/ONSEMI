from django.urls import path
from .views import post_views, upload_views, detail_views

app_name = 'blog_app'

urlpatterns = [
    path("post/", post_views.post_all, name='post_list'),
    path("post/upload/", upload_views.post_upload, name='post_upload'),
    path('post/<int:pk>/', detail_views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', detail_views.post_like, name='post_like'),
    path('post/new/', detail_views.post_create, name='post_create'),
    path('post/<int:post_pk>/comment/new/', detail_views.comment_create, name='comment_create'),
    path('post/<int:pk>/delete/', detail_views.post_delete, name='post_delete'),
    path('post/<int:pk>/edit/', detail_views.post_edit, name='post_edit'),
    path('post/<int:post_pk>/comment/<int:comment_pk>/delete/', detail_views.comment_delete, name='comment_delete'),
    path("post", post_views.post_all, name='post'),
    path("post/upload", upload_views.post_upload, name='upload'),
]