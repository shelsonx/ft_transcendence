from django.urls import path

from .views import index, error_404

urlpatterns = [
    path('', index, name='index'),
    path('404/', error_404, name='index'),
]
