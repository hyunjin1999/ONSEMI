from django.db import models
from auth_app.models import User


class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True, db_column='blog_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    name = models.CharField(db_column='name', max_length=255)
    title = models.TextField(db_column='title')
    content = models.TextField(db_column='content')
    image = models.ImageField(db_column='image', blank=True, null=True)
    datetime = models.DateTimeField(db_column='datetime', auto_now_add=True)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, db_column='comment_id')  
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id') 
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, db_column='blog_id') 
    datetime = models.DateTimeField(db_column='datetime', auto_now_add=True)
    content = models.TextField(db_column='content', blank=False, null=False)


class Love(models.Model):
    love_id = models.AutoField(primary_key=True, db_column='love_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, db_column='blog_id')
    datetime = models.DateTimeField(db_column='datetime', auto_now_add=True)
