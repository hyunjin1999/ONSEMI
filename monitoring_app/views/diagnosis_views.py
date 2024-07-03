from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from management_app.models import Care, Senior
from monitoring_app.models import Diagnosis

def diagnosis_view(request, care_id):
    diagnosis = get_object_or_404(Diagnosis, care_id = care_id)
    care = Care.objects.get(id=care_id)
    #diagnosis = Diagnosis.objects.get(pk=int(care_id))
    senior = Senior.objects.get(id=care_id)
    context = {"senior" : senior, "diagnosis" : diagnosis, "care" : care}
    return render(request, 'monitoring_app/diagnosis.html', context)