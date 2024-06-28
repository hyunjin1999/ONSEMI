from blog_app.models import Blog
from django.shortcuts import render, redirect
from auth_app.models import User
from blog_app.forms import PostForm
from django.contrib.auth.decorators import login_required


# 게시글 업로드 기능
def post_upload(request):
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
        # [추가 구현 필요] 로그인을 하지 않으면 업로드 불가
        if request.user == 'AnonymousUser':
            pass
        
        form = PostForm(instance=post)
        return render(request, 'blog_app/upload.html', {'form': form})
    
    
 
