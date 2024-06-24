from blog_app.models import Blog
from django.shortcuts import render, get_object_or_404, redirect
from auth_app.models import User


def post_upload(request):
    user = get_object_or_404(User, pk=1)
    
    if request.method == 'POST':
        post = Blog(
            user_id=user,
            name=user.username,
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            image=request.POST.get('image'),
        )
        post.save()
        
        return redirect('blog:post')
    else:
        return render(request, 'upload.html')