from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from management_app.models import Report, Care, Senior
from auth_app.models import User

@login_required
def report_list(request):
    sort_by = request.GET.get('sort_by', '-created_at')
    user_id = request.GET.get('user', None)
    senior_ids = request.GET.getlist('senior_ids', None)
    status_filter = request.GET.get('status_filter', 'all')

    reports = Report.objects.all().order_by(sort_by)

    if user_id and user_id != 'None':
        reports = reports.filter(user_id=user_id)
        seniors = Senior.objects.filter(user_id=user_id)
    else:
        seniors = Senior.objects.all()

    if senior_ids:
        senior_ids = [senior_id for senior_id in senior_ids if senior_id]
        
    if senior_ids:
        reports = reports.filter(care__seniors__id__in=senior_ids).distinct()

    if status_filter == 'completed':
        reports = reports.filter(status='등록')
    elif status_filter == 'not_completed':
        reports = reports.filter(status='미등록')

    report_paginator = Paginator(reports, 5)
    report_page_number = request.GET.get('report_page')
    report_page_obj = report_paginator.get_page(report_page_number)

    pending_cares = Care.objects.filter(care_state='APPROVED').exclude(id__in=Report.objects.values('care_id'))
    pending_paginator = Paginator(pending_cares, 5)
    pending_page_number = request.GET.get('pending_page')
    pending_page_obj = pending_paginator.get_page(pending_page_number)

    pending_reports_count = pending_cares.count()

    return render(request, 'management_app/volunteer_report_list.html', {
        'report_page_obj': report_page_obj,
        'pending_page_obj': pending_page_obj,
        'sort_by': sort_by,
        'user_id': user_id,
        'seniors': seniors,
        'selected_senior_ids': senior_ids,
        'status_filter': status_filter,
        'users': User.objects.all(),
        'pending_reports_count': pending_reports_count,
    })