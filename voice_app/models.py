import datetime
from django.db import models

class VoiceData(models.Model):
    audio_file = models.FileField(upload_to='voice_data/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=255, blank=True, null=True)
    care = models.ForeignKey('management_app.Care', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'VoiceData {self.id}'