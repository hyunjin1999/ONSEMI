from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from blog_app.models import Blog, Comment, Like
from blog_app.forms import NoticeForm, CommentForm

# 공지사항 상세보기 기능
@login_required
def notice_detail(request, pk):
    
    # 공지사항 게시글 불러오기
    notice = get_object_or_404(Blog, pk=pk)
    
    # 조회수 증가
    notice.views += 1 
    notice.save()
    
    return render(request, 'blog_app/notice_detail.html', {
        'notice': notice,
    })


# 공지사항 삭제 기능
@login_required
@require_POST
def post_delete(request, pk):
    
    # 삭제할 공지사항 불러오기
    notice = get_object_or_404(Blog, pk=pk)
    
    if notice.user_id != request.user:
        return redirect('blog_app:notice_detail', pk=pk)
    
    notice.delete()
    return redirect('blog_app:notice_list')


# 공지사항 수정 기능
@login_required
def post_edit(request, pk):
    
    # 수정할 게시글 불러오기
    notice = get_object_or_404(Blog, pk=pk)
    
    # 공지사항 작성자가 아니면 수정 불가
    if notice.user_id != request.user:
        return redirect('blog_app:notice_detail', pk=pk)

    # POST방식: 수정된 공지사항 저장 후 수정된 공지사항으로 이동
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user_id = request.user
            notice.save()
            return redirect('blog_app:notice_detail', pk=notice.pk)
        
    # GET방식: 공지사항 수정 폼으로 이동
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'blog_app/notice_edit.html', {'form': form})
