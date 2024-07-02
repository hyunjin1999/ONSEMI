# from django.urls import path
# from . import views

# app_name = 'payment_app'

# urlpatterns = [
#     path('form/', views.payment_form, name='payment_form'),
#     path('complete/', views.payment_complete, name='payment_complete'),
# ]

from django.urls import path
from . import views

app_name = 'payment_app'

urlpatterns = [
    path('form/<int:order_id>/', views.payment_form, name='payment_form'),
    path('success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('fail/<int:order_id>/', views.payment_fail, name='payment_fail'),
]