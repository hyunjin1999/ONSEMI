from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from blog_app.models import Blog, Comment, Like
from blog_app.forms import NoticeForm, CommentForm

@login_required
def notice_detail(request, pk):
    notice = get_object_or_404(Blog, pk=pk)
    notice.views += 1  # 조회수 증가
    notice.save()
    
    return render(request, 'blog_app/notice_detail.html', {
        'notice': notice,
    })

@login_required
def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user_id = request.user
            notice.save()
            return redirect('blog_app:notice_detail', pk=notice.pk)
    else:
        form = NoticeForm()
    return render(request, 'blog_app/notice_create.html', {'form': form})

@login_required
@require_POST
def post_delete(request, pk):
    notice = get_object_or_404(Blog, pk=pk)
    if notice.user_id != request.user:
        return redirect('blog_app:notice_detail', pk=pk)
    
    notice.delete()
    return redirect('blog_app:notice_list')

def post_list(request):
    posts = Blog.objects.all()
    return render(request, 'blog_app/notice_list.html', {'posts': posts})

@login_required
def post_edit(request, pk):
    notice = get_object_or_404(Blog, pk=pk)
    if notice.user_id != request.user:
        return redirect('blog_app:notice_detail', pk=pk)

    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user_id = request.user
            notice.save()
            return redirect('blog_app:notice_detail', pk=notice.pk)
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'blog_app/notice_edit.html', {'form': form})