# Third Party
from django.urls import path

# Local Folder
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.GameView.as_view(), name='game'),
    path('games/<uuid:pk>', views.UserGamesView.as_view(), name='user_games'),
    # path('games', views.UserGamesView.as_view(), name='games'),
]
