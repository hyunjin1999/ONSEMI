from django.urls import path
from . import views

app_name = 'cart_app'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove,
                                     name='cart_remove'),
    path('stock_alert/', views.stock_alert, name='stock_alert'),
]