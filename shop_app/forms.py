from django import forms
from .models import Category, Product, Comment, Star

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment  # 대댓글도 Comment 모델을 사용해야 함
        fields = ['content']

class StarForm(forms.ModelForm):
    class Meta:
        model = Star
        fields = ['rating']

class StarForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select, label="별점")
    
    class Meta:
        model = Star
        fields = ['rating']