# Third Party
from django.urls import path

# Local Folder
from . import views

app_name = "core"
urlpatterns = [
    path("games", views.GamesView.as_view(), name="games"),
    path("user-games/<uuid:pk>", views.GamesView.as_view(), name="user_games"),
    path(
        "view-user-games/<uuid:pk>", views.GamesView.as_view(), name="view_user_games"
    ),
    path("game", views.AddGameView.as_view(), name="add_game"),
    path(
        "game-validation/<int:pk>",
        views.ValidateGameView.as_view(),
        name="validate_game",
    ),
    path("game/<int:pk>", views.GameView.as_view(), name="game"),
    path("tournaments", views.TournamentsView.as_view(), name="tournaments"),
    path("tournaments/<uuid:pk>", views.TournamentsView.as_view(), name="tournaments"),
    path("tournament", views.AddTournamentView.as_view(), name="add_tournament"),
    path("tournament/<int:pk>", views.TournamentView.as_view(), name="tournament"),
    path(
        "tournament-validation/<int:pk>",
        views.ValidateTournamentView.as_view(),
        name="validate_tournament",
    ),
]
