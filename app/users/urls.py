from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_user, name='create_user'),
    path('<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('update/status/<int:user_id>/', views.update_user_status, name='update_user_status'),
    path('update/avatar/<int:user_id>/', views.update_user_avatar, name='update_user_avatar'),
    path('update/nickname/<int:user_id>/', views.update_user_nickname, name='update_user_nickname'),
    path('update/two_factor_enabled/<int:user_id>/', views.update_user_two_factor_enabled,
         name='update_user_two_factor_enabled'),
    path('update/email/<int:user_id>/', views.update_user_email, name='update_user_email'),
    path('all/', views.get_all_users, name='get_all_users'),
    path('delete/<str:user_id>/', views.delete_user, name='delete_user'),
]
