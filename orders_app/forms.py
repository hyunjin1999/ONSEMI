from django import forms
from .models import Order
from management_app.models import Senior

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'phone', 'senior']
        widgets = {
            'phone': forms.TextInput(attrs={'id': 'id_phone'}),
        }

    # 로그인한 보호자가 등록된 노인만 뜨게 수정 
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['senior'].queryset = Senior.objects.filter(user_id=user)

class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone', 'senior']  # 수정 가능한 필드