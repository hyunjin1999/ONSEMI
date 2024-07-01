from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart_app.cart import Cart
from django.contrib.auth.decorators import login_required

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # 주문 생성 후 장바구니 비우기
            cart.clear()
            return redirect('payment_app:payment_form', order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
