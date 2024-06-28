from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
# from .tasks import order_created
from cart_app.cart import Cart
from django.contrib.auth.decorators import login_required

# 주문하는 기능
@login_required
def order_create(request):
    
    # 카트 내역 불러오기
    cart = Cart(request)
    
    # POST방식: 주문자 및 상품 정보 저장
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            return redirect('payment_app:payment_form', order_id=order.id)
        
    # GET방식: 주문 폼 페이지로 이동
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})