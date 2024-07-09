from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from ..models import Product, Comment, Star
from ..forms import CommentForm, StarForm, ReplyForm
from django.views.decorators.http import require_POST

@require_POST
@login_required
def add_comment(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.product = product
        comment.user = request.user
        comment.save()
    return redirect('shop_app:product_detail', id=product_id, slug=slug)

@login_required
@require_POST
def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    form = ReplyForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.parent = parent_comment
        reply.product = parent_comment.product  # 대댓글도 원 댓글의 product 설정
        reply.user = request.user
        reply.save()
    return redirect('shop_app:product_detail', id=parent_comment.product.id, slug=parent_comment.product.slug)

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    product_id = comment.product.id
    slug = comment.product.slug
    if comment.user == request.user or comment.product.user == request.user:
        comment.delete()
    return redirect('shop_app:product_detail', id=product_id, slug=slug)

@login_required
@require_POST
def add_star(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id, slug=slug)
    form = StarForm(request.POST)
    if form.is_valid():
        star = form.save(commit=False)
        star.product = product
        star.user = request.user
        star.save()
    return redirect('shop_app:product_detail', id=product_id, slug=slug)

@login_required
@require_POST
def remove_star(request, star_id):
    star = get_object_or_404(Star, id=star_id)
    product_id = star.product.id
    slug = star.product.slug
    star.delete()
    return redirect('shop_app:product_detail', id=product_id, slug=slug)

@login_required
@require_POST
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return JsonResponse({'likes': comment.total_likes()})