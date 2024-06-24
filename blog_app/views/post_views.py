from blog_app.models import Post
from django.shortcuts import render

def post_all(request):
    post_list = Post.objects.all()
    context = {'post_list': post_list}
    return render(request, 'blog_app/post_list.html', context)

def search(request):
    q = Post.objects.filter(title__contains=request.GET.get('search'))
    context = {'post_list': q}
    print(q)
    return render(request, 'blog_app/post_list.html', context)