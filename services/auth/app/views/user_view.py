from typing import Any
from django.http import HttpResponse, HttpRequest
from django.views import View
from ..exceptions.forbidden_exception import ForbiddenException
from ..interfaces.controllers.base_controller import BaseController
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..decorators.protect_route import ProtectedRoute
from ..validators.validate_user_id import validate_user_id


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    user_controller: BaseController = None

    def __init__(self, user_controller: BaseController) -> None:
        self.user_controller = user_controller

    @ProtectedRoute(func=validate_user_id)
    async def put(self, request: HttpRequest, user_id: str) -> HttpResponse:
        data = await self.user_controller.handle_put(request, user_id)
        return data

    @ProtectedRoute(func=validate_user_id)
    async def delete(self, request: HttpRequest, user_id: str) -> HttpResponse:
        data = await self.user_controller.handle_delete(request, user_id)
        return data
