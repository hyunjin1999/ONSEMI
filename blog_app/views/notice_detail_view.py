from blog_app.models import Blog
from django.shortcuts import render, get_object_or_404

def notice_detail(request, id):
    #notice = get_object_or_404(Blog, id=id) #
    return render(request, 'blog_app/notice_detail.html')# test