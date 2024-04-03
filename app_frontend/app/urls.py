from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

#handler404 = 'singlepage.views.error_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('singlepage.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
