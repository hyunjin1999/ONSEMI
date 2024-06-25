from blog_app.models import Blog
from django.shortcuts import render


# 가정: notices 데이터는 데이터베이스 또는 다른 저장소에 저장되어 있음
notices = [
    {'id': 1, 'title': '공지 제목 1', 'date': '2024-06-24', 'content': '공지 내용 1...'},
    {'id': 2, 'title': '공지 제목 2', 'date': '2024-06-23', 'content': '공지 내용 2...'},
    {'id': 3, 'title': '공지 제목 3', 'date': '2024-06-22', 'content': '공지 내용 3...'},
    {'id': 4, 'title': '공지 제목 4', 'date': '2024-06-21', 'content': '공지 내용 4...'},
    {'id': 5, 'title': '공지 제목 5', 'date': '2024-06-20', 'content': '공지 내용 5...'},
    {'id': 6, 'title': '공지 제목 6', 'date': '2024-06-19', 'content': '공지 내용 6...'},
    {'id': 7, 'title': '공지 제목 7', 'date': '2024-06-18', 'content': '공지 내용 7...'},
    {'id': 8, 'title': '공지 제목 8', 'date': '2024-06-17', 'content': '공지 내용 8...'},
]


def notice_list(request):
    #notices = Blog.objects.all() # test
    return render(request, 'blog_app/notice_list.html', {'notices': notices})


