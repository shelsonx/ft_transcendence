
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('total_infos/', views.total_infos, name='total_infos'),
    path('user/<int:id>/', views.get_user, name='get_user'),
]
