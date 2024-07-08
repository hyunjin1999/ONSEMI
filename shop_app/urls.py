from django.urls import path
from . import views

app_name = 'shop_app'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add_to_recent/<int:id>/', views.add_to_recent_products, name='add_to_recent_products'),
    path('remove_from_recent/<int:id>/', views.remove_from_recent_products, name='remove_from_recent_products'),
]

# from django.urls import path
# from . import views

# app_name = 'shop_app'

# urlpatterns = [
#     path('', views.product_list, name='product_list'),
#     path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
#     path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
# ]