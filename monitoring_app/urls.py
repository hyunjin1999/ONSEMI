from django.urls import path
from .views import order_report_views

app_name = 'monitoring_app'

urlpatterns = [
    path('generate/', order_report_views.generate, name='generate'),
    path('download_csv/', order_report_views.download_csv, name='download_csv'),
]