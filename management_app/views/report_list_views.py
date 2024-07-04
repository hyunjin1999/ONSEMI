from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from management_app.models import Report, Care
from auth_app.models import User

@login_required
def report_list(request):
    sort_by = request.GET.get('sort_by', '-created_at')
    user_id = request.GET.get('user_id', None)
    senior_ids = request.GET.getlist('senior_ids', None)
    status_filter = request.GET.get('status_filter', 'all')

    reports = Report.objects.all().order_by(sort_by)

    if user_id:
        reports = reports.filter(user_id=user_id)
        seniors = Senior.objects.filter(user_id=user_id)
    else:
        seniors = Senior.objects.all()

    if senior_ids:
        reports = reports.filter(care__seniors__id__in=senior_ids).distinct()

    if status_filter == 'completed':
        reports = reports.filter(status='등록완료')
    elif status_filter == 'not_completed':
        reports = reports.filter(status='미등록')

    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 작성해야 할 보고서 개수 계산
    pending_reports_count = Care.objects.filter(care_state='APPROVED').exclude(id__in=Report.objects.values('care_id')).count()

    return render(request, 'management_app/volunteer_report_list.html', {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'user_id': user_id,
        'seniors': seniors,
        'selected_senior_ids': senior_ids,
        'status_filter': status_filter,
        'users': User.objects.all(),
        'pending_reports_count': pending_reports_count,  # 작성해야 할 보고서 개수 전달
    })