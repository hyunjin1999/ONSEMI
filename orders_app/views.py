from django.shortcuts import render, redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart_app.cart import Cart
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from management_app.models import Care


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # 현재 로그인된 사용자를 주문에 연결
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # 주문 생성 후 장바구니 비우기
            cart.clear()

            return redirect('payment_app:payment_form', order_id=order.id)
        
    else:
        form = OrderCreateForm(user=request.user)

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})

@login_required
def export_orders_to_csv(request):
    orders = Order.objects.filter(email=request.user.email, paid=True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Product', 'Price', 'Quantity', 'Total Cost', 'Created'])

    for order in orders:
        for item in order.items.all():
            writer.writerow([order.id, item.product.name, item.price, item.quantity, item.get_cost(), order.created])

    return response
