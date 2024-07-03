from django.db import models
from management_app.models import Senior, Care

class Diagnosis(models.Model):
    senior = models.ForeignKey(Senior, on_delete=models.CASCADE)
    care = models.ForeignKey(Care, on_delete=models.CASCADE, default=1)
    diagnosis_date = models.DateTimeField(auto_now_add=True)
    diagnosis_content = models.CharField(max_length=255)
    to_parents = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.senior.name} - {self.diagnosis_date}"

    class Meta:
        db_table = "diagnosis"
