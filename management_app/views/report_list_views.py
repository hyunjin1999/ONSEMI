from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from auth_app.utils import volunteer_required
from django.core.paginator import Paginator
from management_app.models import Report, Care, Senior
from auth_app.models import User
from django.http import JsonResponse

@login_required
@volunteer_required
def report_list(request):
    user = request.user
    sort_by = request.GET.get('sort_by', '-created_at')
    volunteer_id = request.GET.get('volunteer_id', str(request.user.id))  # 현재 로그인한 봉사자의 ID로 기본값 설정
    senior_ids = request.GET.getlist('senior_ids', ['all'])
    print('처음 페이지에 접근했을 때 senior_ids :', senior_ids)
    status_filter = request.GET.get('status_filter', 'all')

    reports = Report.objects.all().order_by(sort_by)

    # user_type이 'VOLUNTEER'인 봉사자 목록을 가져옴
    volunteers = list(User.objects.filter(user_type='VOLUNTEER').exclude(id=request.user.id).order_by('username').values('id', 'username'))
    current_user = {'id': request.user.id, 'username': request.user.username}
    volunteers.insert(0, current_user)  # 현재 로그인한 사용자를 맨 앞에 추가

    reports = reports.filter(user_id=volunteer_id)

    if 'all' not in senior_ids:
        print('senior_ids (before): ',senior_ids)
        senior_ids_split = senior_ids.split('_')
        senior_ids = senior_ids_split[0]
        print('senior_ids (after): ',senior_ids)
        user_id = senior_ids_split[1]
        print('user_id: ',senior_ids)
        seniors = Senior.objects.filter(id=senior_ids, user_id=user_id).select_related('user_id').values('id', 'name', 'user_id', 'user_id__username')
        reports = reports.filter(care__seniors__id=senior_ids).distinct()
    else:
        user_id = None

    if status_filter == 'completed':
        reports = reports.filter(status='등록')
    elif status_filter == 'not_completed':
        reports = reports.filter(status='미등록')

    seniors = Senior.objects.select_related('user_id').values('id', 'name', 'user_id', 'user_id__username')

    # 봉사자가 보고서를 작성한 어르신들을 먼저 필터링
    written_seniors = Senior.objects.filter(cares_seniors__report__user_id=volunteer_id).distinct().select_related('user_id').values('id', 'name', 'user_id', 'user_id__username').order_by('name')
    # written_seniors에서 ID만 추출
    written_senior_ids = written_seniors.values_list('id', flat=True)
    
    # 보고서를 작성하지 않은 어르신들을 필터링
    unwritten_seniors = Senior.objects.exclude(id__in=written_senior_ids).select_related('user_id').values('id', 'name', 'user_id', 'user_id__username').order_by('name', 'user_id__username')
    # 두 그룹을 합침
    seniors = list(written_seniors) + list(unwritten_seniors)

    # 작성된 보고서를 위한 페이지네이션
    report_paginator = Paginator(reports, 5)
    report_page_number = request.GET.get('report_page')
    report_page_obj = report_paginator.get_page(report_page_number)

    # 작성해야할 보고서를 위한 페이지네이션
    pending_cares = Care.objects.filter(care_state='APPROVED').exclude(id__in=Report.objects.values('care_id')).order_by('-datetime')
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
        'selected_senior_ids': senior_ids, # senior_ids는 단일 값으로 해서 나중에 확인 필요
        'status_filter': status_filter,
        'users': User.objects.all(),
        'pending_reports_count': pending_reports_count,
        'volunteers': volunteers,
        'senior_ids': senior_ids,  # 작성해야 할 보고서를 위한 key value
    })

@login_required
@volunteer_required
def seniors_for_volunteer(request, volunteer_id):
    seniors = Senior.objects.filter(cares_seniors__report__user_id=volunteer_id).distinct().select_related('user_id').values('id', 'name', 'user_id', 'user_id__username')
    return JsonResponse({'seniors': list(seniors)})