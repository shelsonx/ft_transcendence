from typing import Any
from django.http import HttpRequest, JsonResponse
from django.views import View
from ..exceptions.forbidden_exception import ForbiddenException
from ..interfaces.controllers.base_controller import BaseController
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..decorators.protect_route import ProtectedRoute


@method_decorator(csrf_exempt, name="dispatch")
class ForgotPasswordView(View):
    forgot_password_controller: BaseController = None

    def __init__(self, forgot_password_controller: BaseController) -> None:
        self.forgot_password_controller = forgot_password_controller

    async def post(self, request: HttpRequest) -> JsonResponse:
        data = await self.forgot_password_controller.handle_post(request)
        return data
