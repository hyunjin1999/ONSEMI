from blog_app.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def post_all(request):
    post_list = Blog.objects.filter(blog_type='BLOG')
    context = {'post_list': post_list}
    print(request.user)
    return render(request, 'blog_app/post_list.html', context)

@login_required
def search(request):
    query = Blog.objects.filter(title__contains=request.GET.get('search'))
    context = {'post_list': query}
    print(query)
    return render(request, 'blog_app/post_list.html', context)