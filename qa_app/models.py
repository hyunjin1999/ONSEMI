from django.db import models

class ChatHistory(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    query = models.TextField()
    sim1 = models.FloatField()
    sim2 = models.FloatField()
    sim3 = models.FloatField()
    answer = models.TextField()

    def __str__(self):
        return f"Time: {self.datetime}Query: {self.query[:50]}... Answer: {self.answer[:50]}..."