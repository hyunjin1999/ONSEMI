from blog_app.models import *
from django.shortcuts import render

def post_all(request):
    post_list = Blog.objects.filter(blog_type='BLOG')
    context = {'post_list': post_list}
    print(request.user)
    return render(request, 'blog_app/post_list.html', context)


def search(request):
    query = Blog.objects.filter(title__contains=request.GET.get('search'))
    context = {'post_list': query}
    print(query)
    return render(request, 'blog_app/post_list.html', context)