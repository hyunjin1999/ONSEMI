from django.shortcuts import render
from django.views.generic import ListView
from management_app.models import Care, Senior
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from auth_app.utils import family_required
from django.core.paginator import Paginator

# Create your views here.

@login_required
@family_required
def list_senior(request):
    # 현재 로그인한 사용자의 노인 리스트 가져오기
    user_id = request.user.id
    seniors = Senior.objects.filter(user_id=user_id)
    senior_data = []
    
    # 한글화 작업 및 나이 계산
    for senior in seniors:
        senior_data.append({
            'senior': senior,
            'age': calculate_age(senior.birthdate),
            'gender_display': '여성' if senior.gender == 'Female' else '남성',
            'has_alzheimers_display': '유' if senior.has_alzheimers else '무',
            'has_parkinsons_display': '유' if senior.has_parkinsons else '무'
        })
    
    # 페이지네이션 설정
    paginator = Paginator(senior_data, 8)  # 한 페이지에 8명씩 표시
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_seniors': seniors.count(),
    }
    return render(request, 'management_app/user_senior_list.html', context)