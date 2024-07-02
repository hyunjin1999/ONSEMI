from django.contrib import admin
from .models import Blog, Comment

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_id', 'datetime', 'views')
    readonly_fields = ('views', 'datetime')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user_id = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return ('views', 'datetime', 'user_id')


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)