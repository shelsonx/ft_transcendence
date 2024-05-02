# Create your views here.
# Standard Library
import logging
import uuid

# Third Party
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import generic

from core.models import Game
from user.models import User

logger = logging.getLogger("eqlog")


class UserGamesView(generic.ListView):
    model = Game
    ordering = "game_datetime"
    template_name = "user_games.html"
    paginate_by = 20

    # TODO SHEELA: proteger a rota - somente o usuário pode acessar?
    def get(self, request: HttpRequest, pk: uuid, *args, **kwargs) -> HttpResponse:
        self.user = get_object_or_404(User, pk=pk)
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Game]:
        return self.user.games.all()
