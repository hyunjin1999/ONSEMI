from blog_app.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
# 게시글 불러오기
def post_all(request):
    
    # Blog에서 게시글만 불러오기
    post_list = Blog.objects.filter(blog_type='BLOG')
    
    context = {'post_list': post_list}
    return render(request, 'blog_app/post_list.html', context)


@login_required
# 게시글 검색 기능
def search(request):
    query = Blog.objects.filter(title__contains=request.GET.get('search'))
    context = {'post_list': query}
    return render(request, 'blog_app/post_list.html', context)