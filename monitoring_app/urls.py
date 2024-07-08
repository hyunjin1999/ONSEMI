from django.urls import path
from .views import order_report_views, monitor_views, diagnosis_views, download_csv_views, csv_view

app_name = 'monitoring_app'

urlpatterns = [
    path('generate/', order_report_views.generate, name='generate'),
    path('download_order_csv/', download_csv_views.download_order_csv, name='download_order_csv'),
    path('download_care_csv/', download_csv_views.download_care_csv, name='download_care_csv'),
    path('csv_view/', csv_view.csv_view, name='csv_view'),
    path('family_monitor/', monitor_views.family_monitor, name='family_monitor'),
    path('diagnosis/<int:care_id>/', diagnosis_views.diagnosis_view, name='diagnosis'),
]