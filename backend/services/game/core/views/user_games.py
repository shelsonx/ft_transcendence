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


class GamesView(generic.ListView):
    model = Game
    ordering = "game_datetime"
    template_name = "user_games.html"
    paginate_by = 20

    # TODO SHEELA: proteger a rota - somente o usuário pode acessar?
    def get(
        self, request: HttpRequest, pk: uuid = None, *args, **kwargs
    ) -> HttpResponse:
        self.user = None
        if pk:
            self.user = get_object_or_404(User, pk=pk)
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Game]:
        if self.user:
            return self.user.games.all()
        return super().get_queryset()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context
