from django import forms
from blog_app.models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']