from django.urls import path
from .views import order_report_views, monitor_views, download_csv_views, csv_view, monitor_report_list_views

app_name = 'monitoring_app'

urlpatterns = [
    path('generate/', order_report_views.generate, name='generate'),
    path('download_order_csv/', download_csv_views.download_order_csv, name='download_order_csv'),
    path('download_care_csv/', download_csv_views.download_care_csv, name='download_care_csv'),
    path('csv_view/', csv_view.csv_view, name='csv_view'),
    path('family_monitor/', monitor_views.family_monitor, name='family_monitor'),
    path('family_monitor/image/<int:report_id>/', monitor_views.family_monitor_image, name='family_monitor_image'),
    path('family_monitor/report/list/', monitor_report_list_views.report_list, name='report_list'),
    path('family_monitor/report/list/<int:report_id>/', monitor_report_list_views.show_one_report, name='show_one_report'),
    path('family_monitor/poll_signal/', monitor_views.poll_signal, name='poll_signal'),
]