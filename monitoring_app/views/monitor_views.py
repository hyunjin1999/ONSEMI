from django.shortcuts import render,reverse
from management_app.models import Care, Senior
from auth_app.models import User
    
def family_monitor(request):
    sort_by = request.GET.get("sort_by", "datetime")
    order = request.GET.get("order", "asc")
    
    # 현재 로그인한 사용자의 ID
    user_id = request.user.id
    
    if order == "desc":
        sort_by = "-" + sort_by
    
    # 현재 로그인한 사용자의 Care 객체만 필터링
    cares = Care.objects.filter(user_id=user_id)
    
    cares = cares.order_by(sort_by)
    users = User.objects.all()  # 모든 사용자 정보 가져오기
    
    context = {
        "cares": cares,
        "users": users,
        "selected_user": user_id,
    }
    
    return render(request, "monitoring_app/family_monitor.html", context)