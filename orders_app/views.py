from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart_app.cart import Cart
from django.contrib.auth.decorators import login_required
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
            
            # Care 객체 생성
            care_content = "\n".join([f"{item.quantity}x {item.product.name}" for item in order.items.all()])
            Care.objects.create(
                care_type="SHOP",
                user_id=request.user,
                content=care_content,
                title=f'SHOP 서비스 요청 - {order.id}'
            )

            return redirect('payment_app:payment_form', order_id=order.id)
        
    else:
        form = OrderCreateForm(user=request.user)

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})