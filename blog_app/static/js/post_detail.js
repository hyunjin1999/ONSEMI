document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.reply-link').forEach(function(element) {
        element.onclick = function(e) {
            e.preventDefault();
            document.getElementById('parent_id').value = this.getAttribute('data-id');
            window.scrollTo(0, document.body.scrollHeight);
        };
    });

    document.getElementById('like-button').onclick = function(e) {
        e.preventDefault();
        const url = this.getAttribute('data-url');
        const csrfToken = this.getAttribute('data-csrf-token');
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('like-count').textContent = data.likes;
        });
    };

    window.confirmDeletePost = function(postId) {
        if (confirm('정말 포스트를 삭제하시겠습니까?')) {
            const csrfToken = document.querySelector(`button[onclick='confirmDeletePost(${postId})']`).getAttribute('data-csrf-token');
            fetch(`/blog/${postId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            }).then(response => {
                if (response.ok) {
                    window.location.href = '/blog/';
                } else {
                    alert('포스트 삭제에 실패했습니다.');
                }
            });
        }
    };

    window.confirmDeleteComment = function(postId, commentId) {
        if (confirm('정말 댓글을 삭제하시겠습니까?')) {
            const csrfToken = document.querySelector(`button[onclick='confirmDeleteComment(${postId}, ${commentId})']`).getAttribute('data-csrf-token');
            fetch(`/blog/${postId}/comment/${commentId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    alert('댓글 삭제에 실패했습니다.');
                }
            });
        }
    };
});
