from blog_app.models import *
from django.shortcuts import render

def notice_all(request):
    notice_list = Blog.objects.all()
    context = {'notice_list': notice_list}
    print(request.user)
    return render(request, 'blog_app/notice_list.html', context)


def search(request):
    query = Blog.objects.filter(title__contains=request.GET.get('search'))
    context = {'notice_list': query}
    print(query)
    return render(request, 'blog_app/notice_list.html', context)