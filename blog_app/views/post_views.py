from blog_app.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def post_all(request):
    # Blog에서 게시글만 불러오기
    posts = Blog.objects.filter(blog_type='BLOG').order_by('-datetime')

    # 각 게시물의 댓글 수 계산 및 이미지 존재 여부 확인
    post_list = []
    for post in posts:
        comment_count = post.comments.filter(parent__isnull=True).count()
        for comment in post.comments.filter(parent__isnull=True):
            comment_count += comment.replies.count()
        has_image = post.images.exists()
        post_list.append({
            'post': post,
            'comment_count': comment_count,
            'has_image': has_image
        })
    
    # 페이지네이션 적용
    paginator = Paginator(post_list, 10)  # 페이지당 10개씩 표시
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog_app/post_list.html', context)

@login_required
def search(request):
    search_query = request.GET.get('search', '')
    search_method = request.GET.get('search_method', '')
    
    if search_method == 'title':
        query = Blog.objects.filter(blog_type='BLOG', title__icontains=search_query).order_by('-datetime')
    elif search_method == 'writer':
        query = Blog.objects.filter(blog_type='BLOG', name__icontains=search_query).order_by('-datetime')
    elif search_method == 'both':
        query = Blog.objects.filter(blog_type='BLOG').filter(Q(title__icontains=search_query) | Q(name__icontains=search_query)).order_by('-datetime')
    
    # 각 게시물의 댓글 수 계산 및 이미지 존재 여부 확인
    post_list = []
    for post in query:
        comment_count = post.comments.filter(parent__isnull=True).count()
        for comment in post.comments.filter(parent__isnull=True):
            comment_count += comment.replies.count()
        has_image = post.images.exists()
        post_list.append({
            'post': post,
            'comment_count': comment_count,
            'has_image': has_image
        })

    # 페이지네이션 적용
    paginator = Paginator(post_list, 10)  # 페이지당 10개씩 표시
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'post_list': page_obj.object_list
    }
    return render(request, 'blog_app/post_list.html', context)
