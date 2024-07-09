from django import forms
from django.forms import TextInput, Textarea, FileInput
from .models import Blog, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']
        widgets = {
            'title': TextInput(attrs={
                'style': 'width: 95%; height: 30px;',
                'placeholder': '제목을 입력하세요.'
                }),
            
            'content': Textarea(attrs={
                'style': 'resize:none; width: 95%;',
                'placeholder' : '내용을 입력하세요.'
            }),
            
            'image': FileInput(attrs={
                'style': 'width: 95%;',
                'placeholder' : '내용을 입력하세요.'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={
                'style': 'resize:none; width: 95%; height: 100px;',
                'placeholder' : '댓글을 입력하세요.'
            }),
        }


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']
        widgets = {
            'title': TextInput(attrs={
                'style': 'width: 95%; height: 30px;',
                'placeholder': '제목을 입력하세요.'
                }),
            
            'content': Textarea(attrs={
                'style': 'resize:none; width: 95%;',
                'placeholder' : '내용을 입력하세요.'
            }),
            
            'image': FileInput(attrs={
                'style': 'width: 95%;',
                'placeholder' : '내용을 입력하세요.'
            }),
        }