# python std library
import json

# Django
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

# First Party
from common.models import json_response
from user.decorators import JWTAuthentication
from core.forms import PlayerValidationGameForm
from core.models import Game, GamePlayer, GameStatus
from user.models import User


@method_decorator(csrf_exempt, name="dispatch")
class ValidateGameView(generic.View):
    template_name = "game/validate.html"

    @JWTAuthentication()
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        game = Game.objects.filter(pk=pk).first()
        if not game:
            return json_response.not_found()
        if game.owner != request.user:
            return json_response.forbidden()

        left, right = game.players
        player_to_validate: GamePlayer = right if game.owner == left.user else left
        if not player_to_validate.user:
            return json_response.not_found()

        initial = {"user": player_to_validate.user.id}
        context = {
            "game": game,
            "form": PlayerValidationGameForm(initial=initial),
            "user": player_to_validate.user,
            "GameStatus": GameStatus,
        }
        response = render(request, self.template_name, context)
        return response

    @JWTAuthentication()
    def patch(self, request: HttpRequest, pk: int) -> HttpResponse:
        game = Game.objects.filter(pk=pk).first()
        if not game:
            return json_response.not_found("game")
        if game.owner != request.user:
            return json_response.forbidden()
        if game.status != GameStatus.PENDING:
            return json_response.bad_request(f"game {GameStatus(game.status).label}")

        data = json.loads(request.body)
        user_id = data.get("user")
        if not user_id:
            return json_response.bad_request("missing user")
        user = User.get_object(pk=user_id)
        if not user:
            return json_response.not_found("user")

        left, right = game.players
        player_to_validate = right if game.owner == left.user else left
        if not player_to_validate.user:
            return json_response.not_found("user deleted")
        if player_to_validate.user != user:
            return json_response.bad_request("invalid data")

        auth_data = data.get("auth_data")
        if not auth_data:
            return json_response.bad_request("missing auth data")

        is_valid = auth_data.get("is_success")
        status = auth_data.get("status")
        if not is_valid and status == 400:
            form = PlayerValidationGameForm(data)
            form.is_valid()
            form.add_error("token", auth_data.get("error"))
            context = {
                "game": game,
                "form": form,
                "user": user,
                "GameStatus": GameStatus,
            }
            return render(request, self.template_name, context)

        game.status = GameStatus.SCHEDULED
        game.game_datetime = timezone.now()
        game.save()
        return json_response.success(msg="Game validated")
