# Create your views here.
# Standard Library
import logging

# import pprint
import uuid

# Third Party
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse

# from django.utils.translation import gettext_lazy as _
from django.views import generic

from core.models import Tournament, TournamentStatus, TournamentType
from common.models import json_response
from user.decorators import JWTAuthentication
from user.models import DEFAULT_AVATAR, User

logger = logging.getLogger("eqlog")


class TournamentsView(generic.ListView):
    model = Tournament
    ordering = ["-tournament_date", "status"]
    template_name = "tournaments_list.html"
    # paginate_by = 20
    excluded_status = [
        TournamentStatus.INVITATION,
        TournamentStatus.SCHEDULED,
        # TournamentStatus.CANCELED,
    ]

    @JWTAuthentication()
    def get(
        self, request: HttpRequest, pk: uuid = None, *args, **kwargs
    ) -> HttpResponse:
        self.user = None
        if pk:
            self.user = User.get_object(pk=pk)
            if not self.user:
                return json_response.not_found()
            elif self.user != request.user:
                return json_response.forbidden()

        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Tournament]:
        if self.user:
            return self.user.tournaments.all()

        queryset = super().get_queryset()
        return queryset.exclude(status__in=self.excluded_status)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        context["TournamentStatus"] = TournamentStatus

        tournament_list = []
        count = 0
        for tournament in context["tournament_list"]:
            tournament_list.append(self.get_tournament_data(tournament))
            count += 1
        context["tournament_list"] = tournament_list
        context["total_tournaments"] = count
        context["default_avatar"] = f"https://localhost:8006{DEFAULT_AVATAR}"

        return context

    def get_tournament_data(self, tournament: Tournament) -> Tournament:
        tournament.status_label = TournamentStatus(tournament.status).label
        tournament.type_label = TournamentType(tournament.tournament_type).label

        tournament.all_rounds = tournament.rounds.all().aggregate(
            Sum("number_of_games")
        )
        tournament.games_count = tournament.all_rounds["number_of_games__sum"]

        winner = tournament.winner
        tournament.is_winner = False
        if self.user and winner and winner.user:
            tournament.is_winner = self.user.pk == tournament.winner.user.pk

        tournament.is_owner = False
        if self.user and tournament.owner and self.user.pk == tournament.owner.pk:
            tournament.is_owner = True

        return tournament
