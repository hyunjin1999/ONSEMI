from django.contrib import admin
from .models import Senior, Care

class CareAdmin(admin.ModelAdmin):
    list_display = ('care_type', 'datetime', 'title', 'care_state', 'user_id')
    list_filter = ('care_type', 'care_state', 'datetime')
    search_fields = ('title', 'content', 'user_id__username')
    ordering = ('-datetime',)
    readonly_fields = ('care_type', 'datetime', 'title', 'content', 'user_id', 'seniors')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['care_state'].choices = [
            ('APPROVED', '요청 승인 완료'),
            ('REJECT', '요청 거절'),
        ]
        return form

class SeniorAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'birthdate', 'gender', 'phone_number', 'user_id')
    search_fields = ('name', 'address', 'phone_number', 'user_id__username')
    ordering = ('name',)

admin.site.register(Care, CareAdmin)
admin.site.register(Senior, SeniorAdmin)

