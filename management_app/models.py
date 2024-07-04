from django.db import models
from auth_app.models import User
from django.utils import timezone
# Create your models here.


class Senior(models.Model):
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