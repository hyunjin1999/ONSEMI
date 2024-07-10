from django import forms
from .models import Category, Comment

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CommentForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Comment
        fields = ['content', 'rating', 'image']
        labels = {
            'content': '후기',
            'rating': '별점',
            'image' : '사진',
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment  # 대댓글도 Comment 모델을 사용해야 함
        fields = ['content']
        labels = {
            'content': '댓글',
            }