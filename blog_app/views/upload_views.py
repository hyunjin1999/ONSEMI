from blog_app.models import Blog
from django.shortcuts import render, get_object_or_404, redirect
from auth_app.models import User
from blog_app.forms import PostForm

def post_upload(request):
    post = Blog()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
            return redirect('blog_app:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog_app/upload.html', {'form': form})