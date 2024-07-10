# from django.urls import path
# from .views import views, comment_star_views

# app_name = 'shop_app'

# urlpatterns = [
#     path('', views.product_list, name='product_list'),
#     path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
#     path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
#     path('add_to_recent/<int:id>/', views.add_to_recent_products, name='add_to_recent_products'),
#     path('remove_from_recent/<int:id>/', views.remove_from_recent_products, name='remove_from_recent_products'),
#     path('<int:product_id>/add_comment/', comment_star_views.add_comment, name='add_comment'),
#     path('<int:comment_id>/reply_comment/', comment_star_views.reply_comment, name='reply_comment'),
#     path('<int:product_id>/add_star/', comment_star_views.add_star, name='add_star'),
#     path('<int:star_id>/remove_star/', comment_star_views.remove_star, name='remove_star'),
# ]

from django.urls import path
from .views import views, comment_star_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop_app'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add_to_recent/<int:id>/', views.add_to_recent_products, name='add_to_recent_products'),
    path('remove_from_recent/<int:id>/', views.remove_from_recent_products, name='remove_from_recent_products'),
    path('<int:product_id>/<slug:slug>/add_comment/', comment_star_views.add_comment, name='add_comment'),
    path('reply_comment/<int:comment_id>/', comment_star_views.reply_comment, name='reply_comment'),
    path('delete_comment/<int:comment_id>/', comment_star_views.delete_comment, name='delete_comment'),
    path('like_product/<int:product_id>/', views.like_product, name='like_product'),
    path('like_comment/<int:comment_id>/', comment_star_views.like_comment, name='like_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)