from blog_app.models import Blog
from django.shortcuts import render


def post_all(request):
    post_list = Blog.objects.all()
    context = {'post_list': post_list}
    return render(request, 'post_list.html', context)


def search(request):
    query = Blog.objects.filter(title__contains=request.GET.get('search'))
    context = {'post_list': query}
    print(query)
    return render(request, 'post_list.html', context)