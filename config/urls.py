from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('auth_app.urls')),
    path('', include('blog_app.urls', namespace='blog')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)