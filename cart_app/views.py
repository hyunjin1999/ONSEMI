from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop_app.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib.auth.decorators import login_required


# 카트에 담긴 상품 수량 변경 기능
@login_required
@require_POST
def cart_add(request, product_id):
    
    # 카트, 수량 변경할 상품 불러오기
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    # 상품 수량 변경
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        
    return redirect('cart_app:cart_detail')


# 카트에 담긴 상품 삭제 기능
@login_required
@require_POST
def cart_remove(request, product_id):
    
    # 카트, 삭제할 상품 불러오기
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # 카트에서 해당 상품 삭제
    cart.remove(product)
    
    return redirect('cart_app:cart_detail')


# 카트에 담긴 상품 내역 출력 기능
@login_required
def cart_detail(request):
    
    # 카트 불러오기
    cart = Cart(request)
    
    # 카트에 있는 상품별로 폼 생성
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
        
    return render(request, 'cart/detail.html', {'cart': cart})