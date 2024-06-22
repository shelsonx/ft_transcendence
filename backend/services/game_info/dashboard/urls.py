
from django.contrib import admin
from django.urls import path, include
import uuid

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('total_infos/', views.total_infos, name='total_infos'),
    path('user/<int:id>/', views.get_user, name='get_user'),
    #api
    path('register_user/', views.register_user, name='register_user'),
    path('set_status_user/', views.set_status_user, name='set_status_user'),
    path('set_playing_user/', views.set_playing_user, name='set_playing_user'),
    path('update_scores_user/', views.update_scores_user, name='update_scores_user'),
    path('update_user/', views.update_user, name='update_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
]
