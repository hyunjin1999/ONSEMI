from django.shortcuts import render, get_object_or_404, redirect
from cart_app.forms import CartAddProductForm
from ..models import Category, Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..forms import CommentForm, StarForm, ReplyForm
from django.views.decorators.http import require_POST
from orders_app.models import OrderItem

@login_required
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    recent_products_ids = request.session.get('recent_products', [])
    recent_products = Product.objects.filter(id__in=recent_products_ids)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'recent_products': recent_products})

@login_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    stock_alert = product.stock <= 10

    comment_form = CommentForm()
    star_form = StarForm()
    reply_form = ReplyForm()

    # 부모 댓글 필터링
    comments = product.comments.filter(parent__isnull=True)

    # 최근 본 상품에 추가
    recent_products = request.session.get('recent_products', [])
    if product.id not in recent_products:
        recent_products.append(product.id)
        request.session['recent_products'] = recent_products

    # 사용자 구매 여부 확인
    has_purchased = OrderItem.objects.filter(order__user=request.user, product=product).exists()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'stock_alert': stock_alert,
                   'comment_form': comment_form,
                   'star_form': star_form,
                   'reply_form': reply_form,
                   'comments': comments,
                   'has_purchased': has_purchased,})

@login_required
def add_to_recent_products(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=id, available=True)
        recent_products = request.session.get('recent_products', [])
        if product.id not in recent_products:
            recent_products.append(product.id)
            request.session['recent_products'] = recent_products
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


@login_required
def remove_from_recent_products(request, id):
    recent_products = request.session.get('recent_products', [])
    if id in recent_products:
        recent_products.remove(id)
        request.session['recent_products'] = recent_products
    return redirect('shop_app:product_list')

@login_required
@require_POST
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
    else:
        product.likes.add(request.user)
    return JsonResponse({'likes': product.total_likes()})