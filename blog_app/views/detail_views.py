from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from blog_app.models import Blog, Comment, Like
from blog_app.forms import PostForm, CommentForm

# 게시글 상세 보기 기능
@login_required
def post_detail(request, pk):
    
    # 게시글 불러오기
    post = get_object_or_404(Blog, pk=pk)
    
    # 조회수 증가
    post.views += 1  
    post.save()
    
    # 해당 게시글의 댓글 불러오기
    comments = post.comments.filter(parent__isnull=True)
    new_comment = None
    
    # POST 방식: 댓글 저장
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
    
    # GET 방식: 댓글 작성 폼 로드
    else:
        comment_form = CommentForm()

    # 게시글 상세 페이지로 이동
    return render(request, 'blog_app/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })


# 좋아요 기능
@login_required
@require_POST
def post_like(request, pk):
    
    # 게시글 불러오기
    post = get_object_or_404(Blog, pk=pk)
    
    # 이미 있는 객체는 가져오고, 없다면 생성
    like, created = Like.objects.get_or_create(post=post, user_id=request.user)
    
    # 좋아요 기능은 1번만 사용가능하게 해야함
    if not created: 
        like.delete()
    post.likes = post.post_likes.count()
    post.save()
    return JsonResponse({'likes': post.likes})


# 게시글 삭제 기능
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


# 게시글 수정 기능
@login_required
def post_edit(request, pk):
    
    # 수정할 게시글 불러오기
    post = get_object_or_404(Blog, pk=pk)
    
    # 게시글 작성자가 아니면 수정 불가
    if post.user_id != request.user:
        return redirect('blog_app:post_detail', pk=pk)

    # POST방식: 수정된 게시글 저장 후 수정된 게시글로 이동
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
            return redirect('blog_app:post_detail', pk=post.pk)
        
    # GET방식: 게시글 수정 폼으로 이동
    else:
        form = PostForm(instance=post)
    return render(request, 'blog_app/post_edit.html', {'form': form})


# 댓글 삭제 기능
@login_required
@require_POST
def comment_delete(request, post_pk, comment_pk):
    
    # 게시글, 댓글 불러오기
    post = get_object_or_404(Blog, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # 댓글 작성자가 아니면 삭제 불가
    if comment.post != post or (comment.user_id != request.user and post.user_id != request.user):
        return redirect('blog_app:post_detail', pk=post_pk)
    
    comment.delete()
    return redirect('blog_app:post_detail', pk=post_pk)
