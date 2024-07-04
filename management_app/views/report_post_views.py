from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from management_app.models import Senior, Care, Report, ImageUpload, AudioUpload, TextEntry, CheckboxResult
from auth_app.models import User

@login_required
def create_report(request, care_id):
    care = get_object_or_404(Care, id=care_id)
    if care.care_state not in ['approval', 'confirmed']:
        return redirect('report_list')

    if request.method == 'POST':
        report = Report.objects.create(care=care, user=request.user)
        CheckboxResult.objects.create(
            report=report,
            eye='eye' in request.POST,
            teeth='teeth' in request.POST,
            skin='skin' in request.POST,
            back='back' in request.POST,
            other='other' in request.POST,
            other_text=request.POST.get('other_text', ''),
            no_issue='no_issue' in request.POST
        )

        image_files = request.FILES.getlist('images')
        for f in image_files:
            ImageUpload.objects.create(file=f, user=request.user, senior=care.seniors.first(), care=care)

        audio_files = request.FILES.getlist('audios')
        for f in audio_files:
            AudioUpload.objects.create(file=f, user=request.user, senior=care.seniors.first(), care=care)

        doctor_opinion = request.POST.get('doctor_opinion')
        if doctor_opinion:
            TextEntry.objects.create(text=doctor_opinion, report=report, text_type='의사 소견', user=request.user, senior=care.seniors.first(), care=care)

        user_request = request.POST.get('user_request')
        if user_request:
            TextEntry.objects.create(text=user_request, report=report, text_type='보호자 요구', user=request.user, senior=care.seniors.first(), care=care)

        return redirect('manage_report', report_id=report.id)

    return render(request, 'management_app/add_report.html', {'care': care})

@login_required
def manage_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    checkbox_result = get_object_or_404(CheckboxResult, report=report)

    if request.method == 'POST':
        if 'add_image' in request.POST:
            files = request.FILES.getlist('file')
            for f in files:
                ImageUpload.objects.create(file=f, report=report, user=request.user, senior=report.care.seniors.first())
        elif 'add_audio' in request.POST:
            files = request.FILES.getlist('file')
            for f in files:
                AudioUpload.objects.create(file=f, report=report, user=request.user, senior=report.care.seniors.first())
        elif 'add_text' in request.POST:
            doctor_opinion = request.POST.get('doctor_opinion')
            if doctor_opinion:
                TextEntry.objects.create(text=doctor_opinion, report=report, text_type='의사 소견', user=request.user, senior=report.care.seniors.first())
            user_request = request.POST.get('user_request')
            if user_request:
                TextEntry.objects.create(text=user_request, report=report, text_type='보호자 요구', user=request.user, senior=report.care.seniors.first())
        elif 'change_status' in request.POST:
            report.status = request.POST.get('status')
            report.save()
        elif 'update_notes' in request.POST:
            checkbox_result.eye = 'eye' in request.POST
            checkbox_result.teeth = 'teeth' in request.POST
            checkbox_result.skin = 'skin' in request.POST
            checkbox_result.back = 'back' in request.POST
            checkbox_result.other = 'other' in request.POST
            checkbox_result.other_text = request.POST.get('other_text', '')
            checkbox_result.no_issue = 'no_issue' in request.POST
            checkbox_result.save()
        elif 'delete_image' in request.POST:
            image_id = request.POST.get('image_id')
            image = get_object_or_404(ImageUpload, id=image_id, report=report)
            image.delete()
        elif 'delete_audio' in request.POST:
            audio_id = request.POST.get('audio_id')
            audio = get_object_or_404(AudioUpload, id=audio_id, report=report)
            audio.delete()
        elif 'delete_all_images' in request.POST:
            ImageUpload.objects.filter(report=report).delete()
        elif 'delete_all_audios' in request.POST:
            AudioUpload.objects.filter(report=report).delete()
        return redirect('manage_report', report_id=report.id)

    return render(request, 'management_app/update_report.html', {
        'report': report,
        'checkbox_result': checkbox_result,
        'images': report.images.all(),
        'audios': report.audios.all(),
        'texts': report.texts.all(),
    })

@login_required
def delete_file(request, file_type, pk):
    if file_type == 'image':
        file = get_object_or_404(ImageUpload, pk=pk, user=request.user)
    elif file_type == 'audio':
        file = get_object_or_404(AudioUpload, pk=pk, user=request.user)
    file.delete()
    return redirect('manage_report', report_id=file.report.id)

@login_required
def delete_all_files(request, report_id, file_type):
    report = get_object_or_404(Report, pk=report_id)
    if file_type == 'image':
        ImageUpload.objects.filter(report=report).delete()
    elif file_type == 'audio':
        AudioUpload.objects.filter(report=report).delete()
    return redirect('manage_report', report_id=report.id)