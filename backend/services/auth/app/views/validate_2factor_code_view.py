from django.http import HttpResponse, HttpRequest
from django.views import View
from ..interfaces.controllers.base_controller import BaseController
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..decorators.protect_route import ProtectedRoute
from os import environ
from ..constants.env_variables import EnvVariables


@method_decorator(csrf_exempt, name="dispatch")
class Validate2FactorCodeView(View):
    validate_2factor_code_controller: BaseController = None

    def __init__(self, validate_2factor_code_controller: BaseController) -> None:
        self.validate_2factor_code_controller = validate_2factor_code_controller

    async def post(self, request: HttpRequest) -> HttpResponse:
        data = await self.validate_2factor_code_controller.handle_post(request)
        return data

    @ProtectedRoute(secret=environ.get(EnvVariables.TEMPORARY_JWT_SECRET))
    async def put(self, request: HttpRequest) -> HttpResponse:
        data = await self.validate_2factor_code_controller.handle_put(request)
        return data
