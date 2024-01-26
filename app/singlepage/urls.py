from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sections/<int:section_id>/', views.section, name='section'),
]