from blog_app.models import Blog
from django.shortcuts import render, get_object_or_404, redirect
from auth_app.models import User
from blog_app.forms import PostForm
from django.contrib.auth.decorators import login_required



def post_upload(request):
    print(type(request.user))
    post = Blog()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.name = request.user
            post.blog_type = 'BLOG'
            post.save()
            return redirect('blog_app:post_detail', pk=post.pk)
    else:
        if request.user == 'AnonymousUser':
            pass
        form = PostForm(instance=post)
        return render(request, 'blog_app/upload.html', {'form': form})
    
    
 
