from django.shortcuts import render
from django.views.generic import ListView
from management_app.models import Care, Senior
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from auth_app.utils import family_required

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

# class UserCareListView(LoginRequiredMixin, ListView):
#     model = Care
#     template_name = 'management_app/user_care_list.html'  # 템플릿 파일 이름
#     context_object_name = 'cares'  # 템플릿에서 사용할 객체 이름
#     login_url = '/login/'  # 로그인 페이지 URL (필요 시 수정)
#     paginate_by = 10  # 페이지당 항목 수

#     def get_queryset(self):
#         # 로그인한 사용자가 올린 Care만 가져옵니다.
#         queryset = Care.objects.filter(user_id=self.request.user)

#         # care_state 필터링
#         care_state = self.request.GET.get('care_state')
#         if care_state:
#             queryset = queryset.filter(care_state=care_state)

#         # senior_id 필터링
#         senior_id = self.request.GET.get('senior_id')
#         if senior_id:
#             try:
#                 senior = Senior.objects.get(id=senior_id, user_id=self.request.user)
#                 queryset = queryset.filter(seniors=senior)
#             except Senior.DoesNotExist:
#                 queryset = queryset.none()

#         # 정렬 순서 (기본값: 최신순)
#         order = self.request.GET.get('order', 'desc')
#         if order == 'asc':
#             return queryset.order_by('datetime')
#         else:  # default to 'desc'
#             return queryset.order_by('-datetime')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['care_states'] = Care.objects.values_list('care_state', flat=True).distinct()
#         context['seniors'] = Senior.objects.filter(user_id=self.request.user)
#         context['selected_care_state'] = self.request.GET.get('care_state', '')
#         context['selected_senior_id'] = self.request.GET.get('senior_id', '')
#         context['selected_order'] = self.request.GET.get('order', 'desc')
#         return context

@login_required
@family_required
def list_senior(request):
    # 현재 로그인한 사용자의 노인 리스트 가져오기
    user_id = request.user.id
    seniors = Senior.objects.filter(user_id=user_id)
    # 한글화 작업
    for senior in seniors:
        senior.gender_display = '여성' if senior.gender == 'Female' else '남성'
        senior.has_alzheimers_display = '유' if senior.has_alzheimers else '무'
        senior.has_parkinsons_display = '유' if senior.has_parkinsons else '무'
    
    context = {
        'seniors': seniors
    }
    return render(request, 'management_app/user_senior_list.html', context)
