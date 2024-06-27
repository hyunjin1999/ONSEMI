from django.contrib import admin
from django.urls import path, include
from .views.family_list_views import UserCareListView
from .views import family_list_views, family_post_views, volunteer_list_views

urlpatterns = [
    path("add/care/", family_post_views.add_care),
    path("update/care/", family_post_views.update_care),
    path("add/senior/", family_post_views.add_senior),
    path("update/senior", family_post_views.update_senior),
    path('my-cares/', UserCareListView.as_view(), name='user_care_list'),
]
