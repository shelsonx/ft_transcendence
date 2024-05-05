# Third Party
from django.urls import path

# Local Folder
from . import views

app_name = "core"
urlpatterns = [
    path("", views.GameView.as_view(), name="game"),
    path("games", views.GamesView.as_view(), name="games"),
    path("games/<uuid:pk>", views.GamesView.as_view(), name="user_games"),
]
