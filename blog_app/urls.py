from django.urls import path
from .views import post_views, upload_views, detail_views
from .views import notice_detail_view, notice_views

app_name = 'blog_app'

urlpatterns = [
    
    # 게시판 메인 페이지
    path('', post_views.post_all, name='post_list'),
    path("search/", post_views.search, name='search'),
    path('upload/', upload_views.post_upload, name='post_upload'),
    
    # 자유게시판 상세 페이지
    path('<int:pk>/', detail_views.post_detail, name='post_detail'),
    path('<int:pk>/like/', detail_views.post_like, name='post_like'),
    path('<int:pk>/delete/', detail_views.post_delete, name='post_delete'),
    path('<int:pk>/edit/', detail_views.post_edit, name='post_edit'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', detail_views.comment_delete, name='comment_delete'),
    
    # 공지사항 메인페이지
    path('notice_list/', notice_views.notice_all, name='notice_list'),
    path('notice_list/upload/', upload_views.notice_upload, name='notice_upload'),
    path("notice_list/search/", notice_views.notice_search, name='notice_search'),
    
    # 공지사항 상세 페이지
    path('notice_list/<int:pk>/', notice_detail_view.notice_detail, name='notice_detail'),
    path('notice_list/<int:pk>/like/', notice_detail_view.notice_like, name='notice_like'),
    path('notice_list/<int:pk>/delete/', notice_detail_view.notice_delete, name='notice_delete'),
    path('notice_list/<int:pk>/edit/', notice_detail_view.notice_edit, name='notice_edit'),
    path('notice_list/<int:post_pk>/comment/<int:comment_pk>/delete/', notice_detail_view.notice_comment_delete, name='notice_comment_delete'),        
    
]