

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

from django.shortcuts import render, redirect, get_object_or_404
from management_app.models import Care
from auth_app.models import User
from django.contrib.auth.decorators import login_required
from auth_app.utils import volunteer_required
from django.dispatch import Signal
from monitoring_app.signals import my_signal
from django.core.paginator import Paginator

@login_required
@volunteer_required
def care_list(request):
    sort_by = request.GET.get("sort_by", "datetime")
    order = request.GET.get("order", "desc") # 내람차순으로 수정
    user_id = request.GET.get("user", "")

    if order == "desc":
        sort_by = "-" + sort_by

    cares = Care.objects.all()

    if user_id:
        cares = cares.filter(user_id=user_id)
    
    # 케어 타입 or 케어 상태를 기준으로 정렬할 때 기본적으로 최신 care 요청부터 보임
    order_by_fields = [sort_by, '-datetime'] if 'datetime' not in sort_by else [sort_by]

    cares = cares.order_by(sort_by)
    users = User.objects.all()

    # 페이지네이션 설정
    paginator = Paginator(cares, 10)  # 페이지당 10개의 객체를 보여줌
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "cares": cares,
        "users": users,
        "selected_user": user_id,
        "current_sort_by": request.GET.get("sort_by", "datetime"),  # 요청된 sort_by 그대로 전달
        "current_order": request.GET.get("order", "desc"),  # 요청된 order 그대로 전달
    }

    return render(request, "management_app/volunteer_care_list.html", context)


@login_required
@volunteer_required
def status_update(request, care_id):
    care = get_object_or_404(Care, id=care_id)
    
    if request.method == 'POST':
        care.care_state = request.POST.get('state')
        care.save()
        my_signal.send(sender=care, username=care.user_id.username, senior_name=care.seniors.all()[0].name)
        return redirect('/management/care/list/')
    
    context = {
        'care': care
    }
    
    return render(request, "management_app/volunteer_care_status_update.html", context)