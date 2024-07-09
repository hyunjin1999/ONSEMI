from django import forms
from shop_app.models import Category
from management_app.models import Senior, Care

class FilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    category_order = forms.ChoiceField(choices=[], required=False)
    category_service = forms.ChoiceField(choices=[], required=False)
    selected_senior = forms.ChoiceField(choices=[('all', 'All')], required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category_order'].choices = [('all', '전체')] + [(category.name, category.name) for category in Category.objects.all()]

        care_types = Care.objects.values_list('care_type', flat=True).distinct()
        self.fields['category_service'].choices = [('all', '전체')] + [(care_type, care_type) for care_type in care_types]

        if user:
            self.fields['selected_senior'].choices = [('all', 'All')] + [(senior.id, senior.name) for senior in Senior.objects.filter(user_id=user)]