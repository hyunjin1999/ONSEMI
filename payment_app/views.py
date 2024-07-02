from django.shortcuts import render, get_object_or_404, redirect
from orders_app.models import Order, OrderItem
from shop_app.models import Product
from django.contrib import messages

def payment_form(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'payment_app/payment_form.html', context)

def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # 주문된 상품들의 재고를 줄입니다.
    for item in order.items.all():
        product = item.product
        if product.stock >= item.quantity:
            product.stock -= item.quantity
            product.save()
        else:
            messages.error(request, f'{product.name}의 재고가 부족합니다.')
            return redirect('payment_app:payment_fail', order_id=order.id)

    return render(request, 'orders/order/created.html', {'order': order})

def payment_fail(request, order_id):
    return render(request, 'payment_app/payment_fail.html', {'order_id': order_id})

# from django.shortcuts import render, get_object_or_404
# from orders_app.models import Order

# def payment_form(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     context = {
#         'order': order,
#     }
#     return render(request, 'payment_app/payment_form.html', context)

# def payment_success(request, order_id):
#     order = get_object_or_404(Order, id=order_id)

#     # 주문된 상품들의 재고를 줄입니다.
#     for item in order.items.all():
#         product = item.product
#         product.stock -= item.quantity
#         product.save()
        
#     return render(request, 'orders/order/created.html', {'order': order})

# def payment_fail(request, order_id):
#     return render(request, 'payment_app/payment_fail.html', {'order_id': order_id})