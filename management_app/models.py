from django.db import models
from auth_app.models import User
from django.utils import timezone
from voice_app.models import VoiceData
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from datetime import datetime

class Senior(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    has_alzheimers = models.BooleanField(default=False, null=True, blank=True)
    has_parkinsons = models.BooleanField(default=False, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    photo = models.ImageField(upload_to='senior_photos/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "senior"

#UNIQUE constraint failed: care.title, care.user_id
class Care(models.Model):
    care_type = models.CharField(max_length=100)  # SHOP, VISIT
    datetime = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    seniors = models.ManyToManyField("Senior", related_name="cares_seniors")

    CARE_STATE_CHOICES = [
        ('NOT_APPROVED', '요청 승인 대기'),
        ('COMPLETED', '요청 처리 완료'),
        ('APPROVED', '요청 승인 완료'),
        ('REJECT', '요청 거절'),
    ]

    care_state = models.CharField(
        max_length=50, default="요청 승인 대기",  choices=CARE_STATE_CHOICES
    )  # NOT_APPROVED, CONFIRMED, APPROVED, REJECT
    admin_message = models.TextField(blank=True, null=True)  # 관리자가 거절 사유 혹은 요청에 대한 질문이나 전달할 말이 있을 경우를 위해 메시지 필드 추가


    def __str__(self):
        return self.care_type

    class Meta:
        db_table = "care"
        constraints = [
            models.UniqueConstraint(fields=['title', 'user_id'], name='unique_care_request')
        ]


def upload_to(instance, filename):
    today = datetime.today().strftime('%Y%m%d_%H%M%S')
    user_id = instance.user.id
    senior_id = instance.care.seniors.first().id
    care_id = instance.care.id
    extension = filename.split('.')[-1]
    new_filename = f"{today}.{extension}"
    return os.path.join(f'volunteer_report/{user_id}/{care_id}/image', new_filename)


class Report(models.Model):
    care = models.ForeignKey(Care, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='미등록')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    audio_test_result = models.CharField(max_length=255, default='결과 분석 중입니다.')

    # 이상 부위 정보 필드 추가
    no_issue = models.BooleanField(default=False)
    eye = models.BooleanField(default=False)
    teeth = models.BooleanField(default=False)
    skin = models.BooleanField(default=False)
    back = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    other_text = models.CharField(max_length=255, blank=True, null=True)
    doctor_opinion = models.TextField(blank=True, null=True)
    user_request = models.TextField(blank=True, null=True)

    # 이미지 파일 필드 추가
    images = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return f"Report for Care ID {self.care.id}"


@receiver(post_save, sender=Report)
def set_audio_test_result(sender, instance, created, **kwargs):
    if created:
        voice_data = VoiceData.objects.filter(care=instance.care).first()
        if voice_data and voice_data.result:
            instance.audio_test_result = voice_data.result
        else:
            instance.audio_test_result = '결과 분석 중입니다.'
        instance.save()

