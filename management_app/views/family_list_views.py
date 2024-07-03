from django.shortcuts import render
from django.views.generic import ListView
from management_app.models import Care, Senior
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# 1 -> easy
# user(보호자)가 노인을 등록하는 기능 (예상 : html파일 1+개?)
#       -> 위에거 수정하는 페이지(html1개+)


# 2 -> normal
# user(보호자)가 Care를 등록하는 기능(예상 :html파일 1+개?) -> 어려움
#       -> 위에거 수정하는 페이지(html1개+)

# 3 ->개어렵
# user(봉사자)가 user(보호자)가 올린 Care를 확인하는 = 조회하는 기능(예상 :html 1+개?)
# 여러 방면으로 조회할 수 있어야함 ( 노인 카테고리로 조회, 오름차순, 내림차순, or 유저별로, 지역별로, 날짜별로 오름차순)
# NOT_APPROVED, CONFIRMED, APPROVED
# 4 ->hard
# user(보호자)가 자신이 올린 Care를 확인하는 기능(예상: html 1개 이상)
# 여러 방면으로 조회할 수 있어야함
# 위에거랑 같은데 유저별은 없겠죠?

# NOT_APPROVED, CONFIRMED, APPROVED

def list_senior(request):
    # 현재 로그인한 사용자의 노인 리스트 가져오기
    user_id = request.user.id
    seniors = Senior.objects.filter(user_id=user_id)

    context = {
        'seniors': seniors
    }
    return render(request, 'management_app/user_senior_list.html', context)
