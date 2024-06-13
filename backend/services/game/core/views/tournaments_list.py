# Create your views here.
# Standard Library
import logging

# import pprint
import uuid

# Third Party
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

# from django.utils.translation import gettext_lazy as _
from django.views import generic

from core.models import Tournament, TournamentStatus, TournamentType
from user.decorators import JWTAuthentication
from user.models import User

logger = logging.getLogger("eqlog")


class TournamentsView(generic.ListView):
    model = Tournament
    ordering = ["status", "tournament_date"]
    template_name = "tournament_table.html"
    # paginate_by = 20

    # TODO SHEELA: proteger a rota - somente o usuário pode acessar?
    @JWTAuthentication()
    def get(
        self, request: HttpRequest, pk: uuid = None, *args, **kwargs
    ) -> HttpResponse:
        self.user = None
        if pk:
            self.user = get_object_or_404(User, pk=pk)
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Tournament]:
        if self.user:
            return self.user.tournaments.all()
        return super().get_queryset()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        context["TournamentStatus"] = TournamentStatus

        tournament_list = []
        for tournament in context["tournament_list"]:
            tournament_list.append(self.get_tournament_data(tournament))
        context["tournament_list"] = tournament_list

        return context

    def get_tournament_data(self, tournament: Tournament) -> Tournament:
        tournament.status_label = TournamentStatus(tournament.status).label
        tournament.type_label = TournamentType(tournament.tournament_type).label
        tournament.all_rounds = tournament.rounds.all().aggregate(
            Sum("number_of_games")
        )
        tournament.games_count = tournament.all_rounds["number_of_games__sum"]
        return tournament
