# Create your views here.
# Standard Library
import logging

# import pprint
import uuid

# Third Party
from django.db.models import Sum, Q
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
            return self.user.tournaments.all().exclude(
                Q(status__in=[TournamentStatus.INVITATION]) & ~Q(owner=self.user)
            )

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

    def get_tournament_data(self, t: Tournament) -> Tournament:
        t.status_label = TournamentStatus(t.status).label
        t.type_label = TournamentType(t.tournament_type).label

        t.all_rounds = t.rounds.all().aggregate(
            Sum("number_of_games")
        )
        t.games_count = t.all_rounds["number_of_games__sum"] or 0

        winner = t.winner
        t.is_winner = False
        if self.user and winner and winner.user:
            t.is_winner = self.user.pk == t.winner.user.pk

        t.is_owner = False
        if self.user and t.owner and self.user.pk == t.owner.pk:
            t.is_owner = True

        t.current_game = t.get_next_or_current_game()

        return t
