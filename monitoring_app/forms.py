from django import forms
from shop_app.models import Category

class FilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)