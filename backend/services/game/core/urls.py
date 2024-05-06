# Third Party
from django.urls import path

# Local Folder
from . import views

app_name = "core"
urlpatterns = [
    path("games", views.GamesView.as_view(), name="games"),
    path("user/<uuid:pk>/games", views.GamesView.as_view(), name="user_games"),
    path("game", views.GameView.as_view(), name="create_game"),
    path("game/<int:pk>", views.GameView.as_view(), name="game"),
]
