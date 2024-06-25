from django import forms
from .models import Blog, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']