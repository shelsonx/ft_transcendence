# python std library
import uuid
from http import HTTPStatus

# Django
from django.forms import ValidationError
from django.http import (
    HttpRequest,
    HttpResponse,
    QueryDict,
)
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

# First Party
from common.models import json_response
from core.models import (
    Game,
    GameRules,
    GameRuleType,
    GameStatus,
    Round,
    RoundStatus,
    Tournament,
    TournamentPlayer,
    TournamentStatus,
    TournamentType,
    VerificationType,
)
from core.forms import GameRulesForm, TournamentForm, TournamentPlayerForm
from user.decorators import JWTAuthentication
from user.models import User


@method_decorator(csrf_exempt, name="dispatch")
class AddTournamentView(generic.View):
    template_name = "add_tournament.html"
    tournament_form = None
    rules_form = None
    players_forms = None
    base_player_form = TournamentPlayerForm()

    @JWTAuthentication()
    def get(self, request: HttpRequest) -> HttpResponse:
        self.user = request.user
        self.set_forms()
        response = render(request, self.template_name, self.get_context_data())
        return response

    @JWTAuthentication()
    def post(self, request: HttpRequest) -> HttpResponse:
        self.user = request.user
        post_data = request.POST

        is_valid = True
        self.set_forms(post_data)
        context = self.get_context_data()
        forms = [self.rules_form, self.tournament_form, *self.players_forms]
        if not all([form.is_valid() for form in forms]):
            if not self.rules_form.is_valid():
                context["rules_expanded"] = True
            is_valid = False

        for i, p in enumerate(self.players):
            if not p:
                is_valid = False
                msg = _("User does not exist")
                self.players_forms[i].add_error("username", ValidationError(msg))
            if i != 0:
                if p == self.user:
                    is_valid = False
                    msg = _("You can't play against yourself")
                    self.players_forms[i].add_error("username", ValidationError(msg))

        rule_type = post_data.get("rule_type")
        if rule_type and rule_type != str(GameRuleType.PLAYER_POINTS.value):
            context["rules_expanded"] = True

        if not is_valid:
            context["empty"] = False
            return render(request, self.template_name, context)

        rules = GameRules.objects.filter(
            rule_type=self.rules_form.cleaned_data["rule_type"],
            points_to_win=self.rules_form.cleaned_data["points_to_win"],
            game_total_points=self.rules_form.cleaned_data["game_total_points"],
            max_duration=self.rules_form.cleaned_data["max_duration"],
        ).first()
        if rules is None:
            rules = self.rules_form.save()

        t: Tournament = self.tournament_form.save(commit=False)
        t.status = TournamentStatus.INVITATION
        t.rules = rules
        t.owner = self.user
        t.number_of_players = len(self.players)
        t.tournament_date = timezone.now().date()
        t.save()

        for player_form in self.players_forms:
            p: TournamentPlayer = player_form.save(commit=False)
            p.tournament = t
            if p.user == self.user:
                p.verified = True
            p.save()

        receivers = [tp.user.id for tp in t.players if tp.user != t.owner]
        data = {
            "tournament": t.pk,
            "invite": {
                "user_receiver_ids": receivers,
                "user_requester_id": self.user.id,
                "game_id": t.pk,
                "game_type": VerificationType.TOURNAMENT.value,
            },
        }
        return json_response.success(data=data, status=HTTPStatus.CREATED)

    def get_context_data(self, **kwargs) -> dict:
        return {
            "rules_expanded": False,
            "empty": True,
            "user": self.user,
            "type": self.type,
            "TournamentType": TournamentType,
            "rules_form": self.rules_form,
            "tournament_form": self.tournament_form,
            "players_forms": self.players_forms,
            "base_player_form": self.base_player_form,
        }

    def set_forms(self, data: QueryDict = None) -> None:
        initial = {"username": self.user.username}
        if data:
            self.type = data.get("tournament_type")
            usernames = data.get("username").split(",")
            alias_names = data.get("alias_name").split(",")

            self.players = [self.user]
            for username in usernames:
                user = User.get_object(username=username)
                self.players.append(user)

            self.players_forms = []
            for i, p in enumerate(self.players):
                tp = TournamentPlayer(user=p)
                if i == 0:
                    d = {"alias_name": alias_names[i]}
                    self.players_forms.append(
                        TournamentPlayerForm(d, initial=initial, instance=tp)
                    )
                else:
                    d = {
                        "username": p.username if p else usernames[i - 1],
                        "alias_name": alias_names[i],
                    }
                    self.players_forms.append(TournamentPlayerForm(d, instance=tp))
        else:
            owner_form = TournamentPlayerForm(initial=initial)
            self.players_forms = [owner_form]
        self.players_forms[0].fields["username"].disabled = True
        self.players_forms[0].fields["username"].required = False

        self.rules_form = GameRulesForm(data)
        self.type = TournamentType.ROUND_ROBIN
        initial = {}
        if data:
            nb_players = len(self.players)
            initial = {
                "number_of_players": nb_players,
                "number_of_rounds": nb_players - 1 + nb_players % 2,
            }
        self.tournament_form = TournamentForm(data, initial=initial)


@method_decorator(csrf_exempt, name="dispatch")
class TournamentView(generic.View):
    template_name = "tournament.html"

    @JWTAuthentication()
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        self.t = Tournament.objects.filter(pk=pk).first()
        if not self.t:
            return json_response.not_found()

        self.t.is_owner = False
        if self.t.owner == request.user:
            self.t.is_owner = True

        response = render(request, self.template_name, self.get_context_data())
        return response

    @JWTAuthentication()
    def put(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        t = Tournament.objects.filter(pk=pk).first()
        if not t:
            return json_response.not_found()
        if t.owner != request.user:
            return json_response.forbidden()

        valid_status = [TournamentStatus.SCHEDULED, TournamentStatus.ON_GOING]
        if t.status not in valid_status:
            return json_response.forbidden()

        t.status = TournamentStatus.CANCELED
        t.save()

        rounds = t.get_rounds()
        change_status = [GameStatus.SCHEDULED, GameStatus.PAUSED, GameStatus.ONGOING]
        for r in rounds:
            games = r.games.filter(status__in=change_status)
            for g in games:
                g.status = GameStatus.CANCELED
                g.save()

        return json_response.success(msg="Tournament canceled")

    @JWTAuthentication()
    def delete(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        tournament = Tournament.objects.filter(pk=pk).first()
        if not tournament:
            return json_response.not_found()
        if tournament.owner != request.user:
            return json_response.forbidden()
        if tournament.status != TournamentStatus.INVITATION:
            return json_response.forbidden()

        tournament.delete()
        return json_response.success(msg="Tournament deleted")

    def get_context_data(self, **kwargs) -> dict:
        rounds = self.t.get_rounds()
        for r in rounds:
            r: Round
            r.ordered_games = r.games.all().order_by("game_datetime", "-status")
            current_game = r.get_next_or_current_game()
            for g in r.ordered_games:
                g: Game
                g.status_label = GameStatus(g.status).label
                if g.status == GameStatus.TOURNAMENT:
                    g.status_label = GameStatus.SCHEDULED.label

                player_left, player_right = g.players
                player_left.is_winner = False
                player_right.is_winner = False
                winner = g.winner
                if winner is not None:
                    if player_left and winner.pk == player_left.pk:
                        player_left.is_winner = True
                    else:
                        player_right.is_winner = True

                g.player_left = player_left
                g.player_right = player_right
                g.has_winner = bool(winner)

                g.is_current_game = False
                if g == current_game:
                    g.is_current_game = True

        self.t.status_label = TournamentStatus(self.t.status).label
        self.t.type_label = TournamentType(self.t.tournament_type).label
        return {
            "t": self.t,
            "rounds": rounds,
            "TournamentStatus": TournamentStatus,
            "RoundStatus": RoundStatus,
            "GameStatus": GameStatus,
        }
