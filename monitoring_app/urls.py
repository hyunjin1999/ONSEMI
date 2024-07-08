from django.urls import path
from .views import order_report_views, monitor_views, diagnosis_views

app_name = 'monitoring_app'

urlpatterns = [
    path('generate/', order_report_views.generate, name='generate'),
    path('download_order_csv/', order_report_views.download_order_csv, name='download_order_csv'),
    path('download_care_csv/', order_report_views.download_care_csv, name='download_care_csv'),
    path('csv_view/', order_report_views.csv_view, name='csv_view'),
    path('family_monitor/', monitor_views.family_monitor, name='family_monitor'),
    path('family_monitor/image/<int:report_id>/', monitor_views.family_monitor_image, name='family_monitor_image'),
    path('diagnosis/<int:care_id>/', diagnosis_views.diagnosis_view, name='diagnosis'),
]