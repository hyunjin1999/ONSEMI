from django.urls import path
from .views import order_report_views

app_name = 'monitoring_app'

urlpatterns = [
    path('generate/', order_report_views.generate, name='generate'),
    path('download_order_csv/', order_report_views.download_order_csv, name='download_order_csv'),
    path('download_care_csv/', order_report_views.download_care_csv, name='download_care_csv'),
    path('csv_view/', order_report_views.csv_view, name='csv_view'),
]