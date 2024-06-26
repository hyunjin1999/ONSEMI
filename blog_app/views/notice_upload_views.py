from blog_app.models import Blog
from django.shortcuts import render, get_object_or_404, redirect
from auth_app.models import User
from blog_app.forms import NoticeForm
from django.contrib.auth.decorators import login_required

@login_required
def notice_upload(request):
    notice = Blog()
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user_id = request.user
            notice.name = request.user
            notice.blog_type = 'NOTICE'
            notice.save()
            return redirect('blog_app:notice_detail', pk=notice.pk)
    else:
        form = NoticeForm(instance=notice)
        return render(request, 'blog_app/upload.html', {'form': form})
    
    
 
