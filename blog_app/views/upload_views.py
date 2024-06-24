from blog_app.models import Blog
from django.shortcuts import render, get_object_or_404


def post_upload(request):
    user = get_object_or_404(User, pk=request.user)
    
    if request.method.POST:
        post = Blog(
            user_id=request.user,
            name=user.name,
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            image=request.POST.get('image'),
        )
        post.save()
        
    else:
        return render(request, 'blog/upload.html')