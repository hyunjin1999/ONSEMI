# forms.py
from django import forms
from .models import VoiceData

class VoiceDataForm(forms.ModelForm):
    class Meta:
        model = VoiceData
        fields = ['audio_file']