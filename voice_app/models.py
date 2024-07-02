from django.db import models
import datetime

class VoiceData(models.Model):
    audio_file = models.FileField(upload_to='voice_data/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'VoiceData {self.id}'