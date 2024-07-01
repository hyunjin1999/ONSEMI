from blog_app.models import Blog
from django.shortcuts import render, redirect
from blog_app.forms import NoticeForm

# 공지사항 게시글 업로드
# [추가 구현 필요] 공지사항은 ADMIN만 올릴 수 있게 구현
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
    
    
 
