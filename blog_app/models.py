from django.db import models
from auth_app.models import User

class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True, db_column='blog_id')
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    name = models.CharField(db_column='name', max_length=255)
    title = models.TextField(db_column='title')
    content = models.TextField(db_column='content')
    image = models.ImageField(db_column='image', blank=True, null=True)
    datetime = models.DateTimeField(db_column='datetime', auto_now_add=True)

class Love(models.Model):
    love_id = models.AutoField(primary_key=True, db_column='love_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, db_column='blog_id')
    datetime = models.DateTimeField(db_column='datetime', auto_now_add=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return self.text
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')