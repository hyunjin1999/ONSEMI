from django import forms
from shop_app.models import Category
from management_app.models import Senior

class FilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    category_order = forms.ChoiceField(choices=[], required=False)
    category_service = forms.ChoiceField(choices=[('all', '전체'), ('SHOP', '배달'), ('VISIT', '방문')], required=False)
    selected_senior = forms.ChoiceField(choices=[], required=False, label='Select Senior')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_order'].choices = [('all', '전체')] + [(category.name, category.name) for category in Category.objects.all()]
        self.fields['selected_senior'].choices = [('all', 'All')] + [(senior.id, senior.name) for senior in Senior.objects.all()]