from django.shortcuts import render
from management_app.models import Care, Senior, Report, ReportImage

def diagnosis_view(request):
    user_id = request.user.id # 현재 로그인한 사용자의 ID
    order = request.GET.get("order", "desc")
    selected_senior_id = request.GET.get('selected_senior_id', '')
    selected_care_state = request.GET.get('care_state', '')
    selected_order = request.GET.get('order', 'desc')

    # 정렬 기준
    sort_by = request.GET.get("sort_by", "datetime")
    if order == "desc":
        sort_by = "-" + sort_by

    # 현재 로그인한 사용자의 Care 객체만 필터링
    cares = Care.objects.filter(user_id=user_id)
    if selected_senior_id:
        cares = cares.filter(seniors__id=selected_senior_id)
    if selected_care_state:
        cares = cares.filter(care_state=selected_care_state)
    if selected_order == 'asc':
        cares = cares.order_by('datetime')
    else:
        cares = cares.order_by('-datetime')
    
    seniors = Senior.objects.filter(user_id=user_id)
    reports = Report.objects.filter(care__in=cares)
    sorted_reports = reports.order_by('-created_at')  # created_at 등 원하는 필드로 정렬
    
    selected_senior = None
    if selected_senior_id:
        selected_senior = Senior.objects.get(id=selected_senior_id)

    reports_imgs = ReportImage.objects.filter(report__in=reports)
    sorted_reports_imgs = reports_imgs.order_by('-report_id')
    context = {
        "cares": cares, 
        "selected_user": user_id,
        'selected_senior_id': selected_senior_id,
        'selected_care_state': selected_care_state,
        'selected_order': selected_order,
        "seniors": seniors,
        "selected_senior": selected_senior,
        "reports" : sorted_reports,
        "report_imgs" : sorted_reports_imgs,
    }
    return render(request, "monitoring_app/diagnosis.html", context)
