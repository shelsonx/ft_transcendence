# Third Party
from django.urls import path

# Local Folder
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.GameView.as_view(), name='game'),
]
