from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),
    path('user/', include('auth_app.urls')),
    path('blog/', include('blog_app.urls', namespace='blog_app')),
=======
<<<<<<< HEAD
    path("admin/", admin.site.urls),
    path("user/", include("auth_app.urls")),
    path("", include("main_app.urls")),
    path('blog/', include('blog_app.urls', namespace='blog_app')),
>>>>>>> d697aa323d856e4b0c2cfb59ffbf8f06a6813ce6
>>>>>>> 90769b96bb00ed18a1af52f35b34ba0b4e991049
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)