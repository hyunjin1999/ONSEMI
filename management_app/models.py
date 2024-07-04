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
    care_state = models.CharField(
        max_length=50, default="NOT_APPROVED"
    )  # NOT_APPROVED, CONFIRMED, APPROVED

    def __str__(self):
        return self.care_type

    class Meta:
        db_table = "care"

# 이상 부위 체크박스 결과
class CheckboxResult(models.Model):
    report = models.ForeignKey('Report', on_delete=models.CASCADE, related_name='checkbox_results')
    eye = models.BooleanField(default=False)
    teeth = models.BooleanField(default=False)
    skin = models.BooleanField(default=False)
    back = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    other_text = models.CharField(max_length=255, blank=True, null=True)
    no_issue = models.BooleanField(default=False)
    
    def __str__(self):
        return f"CheckboxResult for Report ID {self.report.id}"

# 봉사자가 작성하는 Report
class Report(models.Model):
    care = models.ForeignKey(Care, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='미등록')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for Care ID {self.care.id}"

# 
class TextEntry(models.Model):
    report = models.ForeignKey(Report, related_name='texts', on_delete=models.CASCADE)
    text = models.TextField()
    text_type = models.CharField(max_length=20, choices=[('의사 소견', '의사 소견'), ('보호자 요구', '보호자 요구')])
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    senior = models.ForeignKey(Senior, on_delete=models.CASCADE)
    care = models.ForeignKey(Care, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text_type}: {self.text[:50]}"

# 이미지와 음성 파일을 실제 서버에 upload?하는 역할
def upload_to(instance, filename, folder):
    today = datetime.today().strftime('%Y%m%d_%H%M%S')
    user_id = instance.user.id
    senior_id = instance.senior.id
    care_id = instance.care.id
    extension = filename.split('.')[-1]
    new_filename = f"{today}.{extension}"
    return os.path.join(f'volunteer_report/{user_id}/{senior_id}/{care_id}/{folder}', new_filename)


def image_upload_to(instance, filename):
    return upload_to(instance, filename, 'image')


def audio_upload_to(instance, filename):
    return upload_to(instance, filename, 'voice')

# 이미지 파일 업로드 기록
class ImageUpload(models.Model):
    file = models.FileField(upload_to=image_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    senior = models.ForeignKey(Senior, on_delete=models.CASCADE)
    care = models.ForeignKey(Care, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name

# 오디오 파일 업로드 기록
class AudioUpload(models.Model):
    file = models.FileField(upload_to=audio_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    senior = models.ForeignKey(Senior, on_delete=models.CASCADE)
    care = models.ForeignKey(Care, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name