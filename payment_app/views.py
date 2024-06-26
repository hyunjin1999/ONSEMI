from django.shortcuts import render, get_object_or_404
from orders_app.models import Order

def payment_form(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'payment_app/payment_form.html', context)

def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/created.html', {'order': order})

def payment_fail(request, order_id):
    return render(request, 'payment_app/payment_fail.html', {'order_id': order_id})