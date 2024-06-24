from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'likes', 'views')
    readonly_fields = ('likes', 'views', 'created_date')
    fieldsets = (
        (None, {'fields': ('title', 'content', 'image', 'created_date', 'published_date')}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        # Superusers can edit all fields except 'likes' and 'views'
        if request.user.is_superuser:
            return self.readonly_fields
        return ('likes', 'views', 'created_date', 'published_date', 'author')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)