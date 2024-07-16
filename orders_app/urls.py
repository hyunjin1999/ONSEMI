from django.urls import path
from . import views

app_name = 'orders_app'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('csv/', views.export_orders_to_csv, name='export_orders_to_csv'),    
    path('my_orders/', views.my_orders, name='my_orders'),  # 주문 목록
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),  # 주문 상세
    path('order/edit/<int:order_id>/', views.order_edit, name='order_edit'),  # 주문 수정
    path('order/cancel/<int:order_id>/', views.order_cancel, name='order_cancel'),  # 주문 취소
]