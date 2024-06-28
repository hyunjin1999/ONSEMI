from django.shortcuts import render, get_object_or_404
from orders_app.models import Order

# 결제 페이지로 이동하는 기능
def payment_form(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'payment_app/payment_form.html', context)


# 결제 성공시 보여지는 페이지
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id) # 주문 정보 불러오기
    return render(request, 'orders/order/created.html', {'order': order})


# 결제 실패시 보여지는 페이지
def payment_fail(request, order_id):
    return render(request, 'payment_app/payment_fail.html', {'order_id': order_id})