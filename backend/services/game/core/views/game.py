# python std library
from datetime import timedelta
from http import HTTPStatus
import json
import logging
import uuid

# Django
from django.forms import ValidationError
from django.http import (
    HttpRequest,
    HttpResponse,
    QueryDict,
)
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

# First Party
from common.models import json_response
from user.decorators import JWTAuthentication
from core.models import Game, GameStatus, GameRules
from core.forms import GameForm, GameRulesForm, UpdateGameForm, UpdateGamePlayerForm
from user.forms import UserSearchForm
from user.models import User


@method_decorator(csrf_exempt, name="dispatch")  # remove csrf protection...
class AddGameView(generic.View):
    template_name = "add_game.html"
    rules_form = None
    user_form = None

    @JWTAuthentication()
    def get(self, request: HttpRequest) -> HttpResponse:
        self.set_forms()
        response = render(request, self.template_name, self.get_context_data())
        return response

    # @csrf_protect
    @JWTAuthentication()
    def post(self, request: HttpRequest) -> HttpResponse:
        post_data = request.POST
        self.set_forms(post_data)
        context = self.get_context_data()
        forms = [self.rules_form, self.user_form]
        if not self.opponent:
            [form.is_valid() for form in forms]
            self.user_form.add_error(
                "username", ValidationError(message="user does not exist")
            )
            return render(request, self.template_name, context)
        if not all(form.is_valid() for form in forms):
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
            "status": GameStatus.SCHEDULED,  # TODO: deixar como PENDING
            "rules": rules,
        }
        game_form = GameForm(data)
        if not game_form.is_valid():
            message = _("An internal error occured while creating the game")
            log = message + ": " + game_form.errors.as_text()
            logging.error(log)  # TODO: remove it!
            return json_response.error(msg=message)

        game: Game = game_form.save(commit=False)
        game.owner = request.user
        game.save()
        game.add_player(request.user)
        game.add_player(self.opponent)
        game.set_players_position()

        data = {"status": "success", "data": {"game": game.pk}}
        return json_response.success(data=data, status=HTTPStatus.CREATED)

    def get_opponent(self, post_data: QueryDict | None) -> User | None:
        opponent = post_data.get("username") if post_data else None
        if opponent:
            opponent = User.get_object(username=opponent)
        return opponent

    def get_context_data(self, **kwargs) -> dict:
        return {
            "invalid": False,
            "GameStatus": GameStatus,
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

        game_form.save()
        left_form.save()
        right_form.save()
        return json_response.success(msg="Game updated")

    @JWTAuthentication()
    def delete(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        game = Game.objects.filter(pk=pk).first()
        if not game:
            return json_response.not_found()
        if game.owner != request.user:
            return json_response.forbidden()

        game.delete()
        return json_response.success(msg="Game deleted")
