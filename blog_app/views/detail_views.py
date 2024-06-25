from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from blog_app.models import Blog, Comment, Like
from blog_app.forms import PostForm, CommentForm

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.views += 1  # 조회수 증가
    post.save()
    
    comments = post.comments.filter(parent__isnull=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user_id = request.user  # 로그인한 사용자 설정
            new_comment.post = post
            parent_id = request.POST.get('parent_id')
            if parent_id:
                new_comment.parent = Comment.objects.get(id=parent_id)
            new_comment.save()
            return redirect('blog_app:post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog_app/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })

@login_required
@require_POST
def post_like(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    user = request.user
    like, created = Like.objects.get_or_create(post=post, user_id=user)
    if not created: # 좋아요 기능은 1번만 사용가능하게 해야함
        like.delete()
    post.likes = post.post_likes.count()
    post.save()
    return JsonResponse({'likes': post.likes})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
            return redirect('blog_app:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog_app/post_create.html', {'form': form})

@login_required
@require_POST
def comment_create(request, post_pk):
    post = get_object_or_404(Blog, pk=post_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.user_id = request.user  # 현재 로그인한 사용자를 설정
        parent_id = request.POST.get('parent_id')
        if parent_id:
            new_comment.parent = Comment.objects.get(pk=parent_id)
        new_comment.post = post
        new_comment.save()
    return redirect('blog_app:post_detail', pk=post_pk)

@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if post.user_id != request.user:
        return redirect('blog_app:post_detail', pk=pk)
    
    post.delete()
    return redirect('blog_app:post_list')

def post_list(request):
    posts = Blog.objects.all()
    return render(request, 'blog_app/post_list.html', {'posts': posts})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if post.user_id != request.user:
        return redirect('blog_app:post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
            return redirect('blog_app:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog_app/post_edit.html', {'form': form})

@login_required
@require_POST
def comment_delete(request, post_pk, comment_pk):
    post = get_object_or_404(Blog, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.post != post or (comment.user_id != request.user and post.user_id != request.user):
        return redirect('blog_app:post_detail', pk=post_pk)
    
    comment.delete()
    return redirect('blog_app:post_detail', pk=post_pk)