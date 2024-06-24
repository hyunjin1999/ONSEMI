from blog_app.models import Blog
from django.shortcuts import render


def post_all(request):
    post_list = Blog.objects.all()
    context = {'post_list': post_list}
    return render(request, 'blog/post_list.html', context)


def search(request):
    q = Blog.objects.filter(title__contains=request.GET.get('search'))
    context = {'post_list':q}
    print(q)
    return render(request, 'blog/post_view.html', context)