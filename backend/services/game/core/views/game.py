# python std library
from datetime import timedelta
from http import HTTPStatus
import json
import uuid

# Django
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

# First Party
from common.models import json_response
from user.decorators import JWTAuthentication
from core.models import (
    Game,
    GameStatus,
    GameRules,
    GameRuleType,
    Tournament,
    TournamentStatus,
    VerificationType,
)
from core.forms import GameForm, GameRulesForm, UpdateGameForm, UpdateGamePlayerForm
from user.forms import UserSearchForm
from user.models import User


@method_decorator(csrf_exempt, name="dispatch")
class AddGameView(generic.View):
    template_name = "add_game.html"
    rules_form = None
    user_form = None

    @JWTAuthentication()
    def get(self, request: HttpRequest) -> HttpResponse:
        self.set_forms()
        response = render(request, self.template_name, self.get_context_data())
        return response

    @JWTAuthentication()
    def post(self, request: HttpRequest) -> HttpResponse:
        post_data = request.POST

        is_valid = True
        self.set_forms(post_data)
        context = self.get_context_data()
        forms = [self.rules_form, self.user_form]
        if not all(form.is_valid() for form in forms):
            if not self.rules_form.is_valid():
                context["rules_expanded"] = True
            is_valid = False

        if not self.opponent:
            [form.is_valid() for form in forms]
            msg = _("User does not exist")
            self.user_form.add_error("username", ValidationError(message=msg))
            is_valid = False

        if self.opponent == request.user:
            [form.is_valid() for form in forms]
            msg = _("You can't play against yourself")
            self.user_form.add_error("username", ValidationError(message=msg))
            is_valid = False

        rule_type = post_data.get("rule_type")
        if rule_type and rule_type != str(GameRuleType.PLAYER_POINTS.value):
            context["rules_expanded"] = True

        if not is_valid:
            return render(request, self.template_name, context)

        rules = GameRules.objects.filter(
            rule_type=self.rules_form.cleaned_data["rule_type"],
            points_to_win=self.rules_form.cleaned_data["points_to_win"],
            game_total_points=self.rules_form.cleaned_data["game_total_points"],
            max_duration=self.rules_form.cleaned_data["max_duration"],
        ).first()
        if rules is None:
            rules = self.rules_form.save()

        data = {
            "status": GameStatus.PENDING,
            "rules": rules,
        }
        game_form = GameForm(data)
        if not game_form.is_valid():
            msg = _("An internal error occured while creating the game")
            return json_response.error(msg=msg)

        game: Game = game_form.save(commit=False)
        game.owner = request.user
        game.save()
        game.add_player(request.user)
        game.add_player(self.opponent)
        game.set_players_position()

        data = {
            "game": game.pk,
            "invite": {
                "user_receiver_ids": [self.opponent.id],
                "user_requester_id": request.user.id,
                "game_id": game.pk,
                "game_type": VerificationType.GAME.value,
            },
        }
        return json_response.success(data, status=HTTPStatus.CREATED)

    def get_opponent(self, post_data: QueryDict | None) -> User | None:
        opponent = post_data.get("username") if post_data else None
        if opponent:
            opponent = User.get_object(username=opponent)
        return opponent

    def get_context_data(self, **kwargs) -> dict:
        return {
            "rules_expanded": False,
            "rules_form": self.rules_form,
            "user_form": self.user_form,
        }

    def set_forms(self, data=None) -> None:
        self.opponent = self.get_opponent(data)
        self.rules_form = GameRulesForm(data)
        self.user_form = UserSearchForm(data, instance=self.opponent)


@method_decorator(csrf_exempt, name="dispatch")
class GameView(generic.View):
    @JWTAuthentication()
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        game = Game.objects.filter(pk=pk).first()
        if not game:
            return json_response.not_found()
        if game.owner != request.user:
            return json_response.forbidden()

        return json_response.success({"game": game.to_json()})

    @JWTAuthentication()
    def patch(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        game = Game.objects.filter(pk=pk).first()

        if not game:
            return json_response.not_found()
        if game.owner != request.user:
            print(game.owner, request.user)
            return json_response.forbidden()

        data = json.loads(request.body)
        data["game_datetime"] = timezone.datetime.fromisoformat(data["game_datetime"])
        duration = data["duration"]
        data["duration"] = timedelta(
            minutes=duration["minutes"], seconds=duration["seconds"]
        )
        game_form = UpdateGameForm(data, instance=game)

        player_left, player_right = game.players
        left_form = UpdateGamePlayerForm(data["player_left"], instance=player_left)
        right_form = UpdateGamePlayerForm(data["player_right"], instance=player_right)

        if not all([game_form.is_valid(), left_form.is_valid(), right_form.is_valid()]):
            return json_response.bad_request("invalid data")
        if data["player_left"]["user"]["id"] != str(player_left.user.pk):
            return json_response.bad_request("compromised data")
        if data["player_right"]["user"]["id"] != str(player_right.user.pk):
            return json_response.bad_request("compromised data")

        game: Game = game_form.save()
        left_form.save()
        right_form.save()

        t = data.get("tournament")
        if t:
            t = Tournament.objects.filter(pk=t).first()
            if t and t.status == TournamentStatus.SCHEDULED:
                t.status = TournamentStatus.ON_GOING
                t.save()

        data = {}
        if game.status == GameStatus.ENDED.value:
            round = game.round.all().first()
            if round is not None:
                game.update_tournament()
            else:
                game.update_users()

            # esure to get data updated
            users_pk = [player_left.user.pk, player_right.user.pk]
            users = User.objects.filter(pk__in=users_pk)
            game = Game.objects.get(pk=game.pk)
            data = {
                "game": game.to_json(),
                "stats": [u.to_stats() for u in users],
            }

        # print("game status: ", GameStatus(game.status).label)
        return json_response.success(data, msg="Game updated")

    @JWTAuthentication()
    def put(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        game = Game.objects.filter(pk=pk).first()

        if not game:
            return json_response.not_found()
        if game.owner != request.user:
            return json_response.forbidden()

        valid_status = [GameStatus.SCHEDULED, GameStatus.PAUSED, GameStatus.ONGOING]
        if game.status not in valid_status:
            return json_response.forbidden()

        game.status = GameStatus.CANCELED
        game.save()
        return json_response.success(msg="Game canceled")

    @JWTAuthentication()
    def delete(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        game = Game.objects.filter(pk=pk).first()
        if not game:
            return json_response.not_found()
        if game.owner != request.user:
            return json_response.forbidden()
        if game.status != GameStatus.PENDING:
            return json_response.forbidden()

        game.delete()
        return json_response.success(msg="Game deleted")
