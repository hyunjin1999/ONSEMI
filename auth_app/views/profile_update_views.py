from django.shortcuts import render

from auth_app.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
# 회원가입 -> template, 비밀번호가 2개가
# 로그인 -> form에 아무것도 입력안했을 떄? 어떻게해야할지
# 로그아웃 -> 1초

# 계정확인  -> views -> templates로 context( views가 templates에게 데이터 전달 )-> templates를 꾸미기

# 계정 수정 -> views -> templates로 context( views가 templates에게 데이터 전달 )-> 변경사항 꾸미기

# 계정 삭제 -> 1초


# @login_required
# def show_profile(request):

#     user = request.user

#     context = {"user": user}

#     return render(request, "auth_app/profile.html", context)
