from django.shortcuts import render, get_object_or_404
from cart_app.forms import CartAddProductForm
from .models import Category, Product
from django.contrib.auth.decorators import login_required

# 상품 리스트 출력 기능
@login_required
def product_list(request, category_slug=None):
    
    # 카테고리를 선택하지 않은 경우: 모든 상품 출력
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # 카테고리를 선택한 경우: 선택한 카테고리 상품만 출력
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


# 상품 상세보기 기능
@login_required
def product_detail(request, id, slug):
    
    # 해당 상품 불러오기
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    
    # 장바구니에 담을 수량 선택 폼
    cart_product_form = CartAddProductForm()
    
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})