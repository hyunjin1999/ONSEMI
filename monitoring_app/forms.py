from django import forms
from shop_app.models import Category

class FilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    category_order = forms.ChoiceField(choices=[], required=False)
    category_service = forms.ChoiceField(choices=[('all', '전체'), ('SHOP', '배달'), ('VISIT', '방문')], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_order'].choices = [('all', '전체')] + [(category.name, category.name) for category in Category.objects.all()]