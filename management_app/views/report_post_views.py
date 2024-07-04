from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from management_app.models import Senior, Care, Report
from voice_app.models import VoiceData
from auth_app.models import User

@login_required
def create_report(request, care_id):
    care = get_object_or_404(Care, id=care_id)
    if care.care_state not in ['APPROVED']:
        return redirect('report_list')

    if request.method == 'POST':
        report = Report.objects.create(care=care, user=request.user)

        voice_data = VoiceData.objects.filter(care=care).first()
        if voice_data and voice_data.result:
            report.audio_test_result = voice_data.result
        else:
            report.audio_test_result = '결과 분석 중입니다.'

        # 이미지 파일 업로드
        image_files = request.FILES.getlist('images')
        for f in image_files:
            report.images = f

        # 텍스트 입력
        report.doctor_opinion = request.POST.get('doctor_opinion', '')
        report.user_request = request.POST.get('user_request', '')

        # 이상 부위 체크박스 결과 저장
        report.no_issue = 'no_issue' in request.POST
        report.eye = 'eye' in request.POST
        report.teeth = 'teeth' in request.POST
        report.skin = 'skin' in request.POST
        report.back = 'back' in request.POST
        report.other = 'other' in request.POST
        report.other_text = request.POST.get('other_text', '')

        report.save()
        return redirect('manage_report', report_id=report.id)

    return render(request, 'management_app/add_report.html', {'care': care})

@login_required
def manage_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        if 'add_image' in request.POST:
            files = request.FILES.getlist('file')
            for f in files:
                report.images = f
        elif 'update_text' in request.POST:
            report.doctor_opinion = request.POST.get('doctor_opinion', '')
            report.user_request = request.POST.get('user_request', '')
        elif 'change_status' in request.POST:
            report.status = request.POST.get('status')
            report.save()
        elif 'update_notes' in request.POST:
            report.no_issue = 'no_issue' in request.POST
            report.eye = 'eye' in request.POST
            report.teeth = 'teeth' in request.POST
            report.skin = 'skin' in request.POST
            report.back = 'back' in request.POST
            report.other = 'other' in request.POST
            report.other_text = request.POST.get('other_text', '')
            report.save()
        elif 'delete_image' in request.POST:
            report.images.delete()
        return redirect('manage_report', report_id=report.id)

    return render(request, 'management_app/update_report.html', {
        'report': report,
        'images': report.images,
    })
