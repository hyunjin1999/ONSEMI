from django.contrib import admin
from .models import Blog, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'datetime', 'views')
    readonly_fields = ('views', 'datetime')
    fieldsets = (
        (None, {'fields': ('title', 'content', 'image', 'datetime')}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        # Superusers can edit all fields except 'likes' and 'views'
        if request.user.is_superuser:
            return self.readonly_fields
        return ('views', 'datetime', 'name')

admin.site.register(Blog, PostAdmin)
admin.site.register(Comment)