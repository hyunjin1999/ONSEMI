from django import forms
from django.forms import TextInput, Textarea, FileInput, modelformset_factory
from .models import Blog, Comment, BlogImage

class PostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        widgets = {
            'title': TextInput(attrs={
                'style': 'width: 97%; height: 30px;',
                'placeholder': '제목을 입력하세요.'
                }),
            'content': Textarea(attrs={
                'style': 'resize:none; width: 97%;',
                'placeholder' : '내용을 입력하세요.'
            }),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = BlogImage
        fields = ['image']
        widgets = {
            'image': FileInput(attrs={
                'style': 'width: 95%;',
            }),
        }

ImageFormSet = modelformset_factory(BlogImage, form=ImageForm, extra=1)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={
                'style': 'resize:none; width: 97%; height: 50px;',
                'placeholder' : '댓글을 입력하세요.'
            }),
        }
        labels = {
            'content': '',
        }