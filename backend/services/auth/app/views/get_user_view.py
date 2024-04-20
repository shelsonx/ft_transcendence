from typing import Any
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views import View
from ..exceptions.forbidden_exception import ForbiddenException
from ..interfaces.controllers.base_controller import BaseController
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..decorators.protect_route import ProtectedRoute


@method_decorator(csrf_exempt, name="dispatch")
class GetUserView(View):
    user_controller: BaseController = None

    def __init__(self, user_controller: BaseController) -> None:
        self.user_controller = user_controller

    @ProtectedRoute()
    async def get(self, request: HttpRequest) -> JsonResponse:
        user_id = request.current_user.sub
        data = await self.user_controller.handle_get(request, user_id)
        return data
