from django.contrib import admin
from django.urls import path, include


from .views.family_list_views import UserCareListView
from .views import family_list_views, family_post_views, volunteer_list_views, report_post_views, report_list_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("add/care/", family_post_views.add_care, name='add_care'),
    path("care/update/<int:care_id>/", family_post_views.update_care, name='update_care'),
    path("care/delete/<int:care_id>/", family_post_views.delete_care, name='delete_care'),
    path("add/senior/", family_post_views.add_senior, name='add_senior'),
    path("care/detail/<int:care_id>/", family_post_views.show_one_care, name='care_detail'),
    path("senior/update/<int:id>/", family_post_views.update_senior, name='update_senior'),
    path("senior/delete/<int:id>/", family_post_views.delete_senior, name='delete_senior'),

    path("senior/list/", family_list_views.list_senior),
    path("care/list/", volunteer_list_views.care_list),
    path("care/list/status/update/<int:care_id>/", volunteer_list_views.status_update),
    # 전체 보고서 목록 조회 및 필터링
    path('report/list/', report_list_views.report_list, name='report_list'),
    # 새로운 보고서 생성
    path('report/create/<int:care_id>/', report_post_views.create_report, name='create_report'),
    # 기존 보고서 관리
    path('report/manage/<int:report_id>/', report_post_views.manage_report, name='manage_report'),
    # 파일 삭제
    path('report/delete/<str:file_type>/<int:pk>/', report_post_views.delete_file, name='delete_file'),
    # 모든 파일 삭제
    path('report/delete_all/<int:report_id>/<str:file_type>/', report_post_views.delete_all_files, name='delete_all_files'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)