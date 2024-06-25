from django.urls import path
from .views import post_views, upload_views, detail_views
from .views import notice_detail_view, notice_list_views
from django.views.generic.base import RedirectView

app_name = 'blog_app'

urlpatterns = [
    path('', post_views.post_all, name='post_list'),
    path('upload/', upload_views.post_upload, name='post_upload'),
    path("search/", post_views.search, name='search'),
    path('<int:pk>/', detail_views.post_detail, name='post_detail'),
    path('<int:pk>/like/', detail_views.post_like, name='post_like'),
    path('<int:post_pk>/comment/new/', detail_views.comment_create, name='comment_create'),
    path('<int:pk>/delete/', detail_views.post_delete, name='post_delete'),
    path('<int:pk>/edit/', detail_views.post_edit, name='post_edit'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', detail_views.comment_delete, name='comment_delete'),
    path("notice_list/", notice_list_views.notice_list, name = "notice_list"),
    path("notice_list/notice_detail/<int:id>/", notice_detail_view.notice_detail, name = "notice_detail"),
    path('search/upload/', RedirectView.as_view(url='/blog/upload/', permanent=False), name='redirect_to_upload'),
]