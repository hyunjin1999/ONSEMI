from blog_app.models import *
from django.shortcuts import render, get_object_or_404

def notice_all(request):
    # notice_list = get_object_or_404()
    notice_list = Blog.objects.filter(blog_type='NOTICE')
    context = {'notice_list': notice_list}
    print(request.user)
    return render(request, 'blog_app/notice_list.html', context)


def search(request):
    query = Blog.objects.filter(title__contains=request.GET.get('search'))
    context = {'notice_list': query}
    print(query)
    return render(request, 'blog_app/notice_list.html', context)