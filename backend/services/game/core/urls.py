# Third Party
from django.urls import path

# Local Folder
from . import views

app_name = "core"
urlpatterns = [
    path("games", views.GamesView.as_view(), name="games"),
    path("user/<uuid:pk>/games", views.GamesView.as_view(), name="user_games"),
    path("add-game", views.AddGameView.as_view(), name="add_game"),
    path("game/<int:pk>", views.GameView.as_view(), name="game"),
    path("tournaments", views.TournamentsView.as_view(), name="tournaments"),
    path(
        "user/<uuid:pk>/tournaments",
        views.TournamentsView.as_view(),
        name="user_tournaments",
    ),
    path("tournament", views.TournamentView.as_view(), name="create_tournament"),
    path("tournament/<int:pk>", views.TournamentView.as_view(), name="tournament"),
]
