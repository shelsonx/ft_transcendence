from typing import Any
from django.http import HttpResponse, HttpRequest,JsonResponse
from django.views import View
from ..interfaces.controllers.base_controller import BaseController
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..decorators.protect_route import ProtectedRoute

@method_decorator(csrf_exempt, name='dispatch')
class SignInView(View):
    sign_in_controller: BaseController = None

    def __init__(self, sign_in_controller: BaseController) -> None:
       self.sign_in_controller = sign_in_controller
       
    async def post(self, request: HttpRequest) -> JsonResponse:
        data = await self.sign_in_controller.handle_post(request)
        return data
