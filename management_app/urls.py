from django.contrib import admin
from django.urls import path, include
from .views import family_list_views, family_post_views, volunteer_list_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("add/care/", family_post_views.add_care),
    path("care/update/<int:care_id>/", family_post_views.update_care),
    path("care/delete/<int:care_id>/", family_post_views.delete_care, name='delete_care'),
    path("add/senior/", family_post_views.add_senior),
    path("care/detail/<int:care_id>/", family_post_views.show_one_care),
    path("senior/update/<int:id>/", family_post_views.update_senior),
    path("senior/delete/<int:id>/", family_post_views.delete_senior, name='delete_senior'),
    path("senior/list/", family_list_views.list_senior),
    path("care/list/", volunteer_list_views.care_list),
    path("care/list/status/update/<int:care_id>/", volunteer_list_views.status_update),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)