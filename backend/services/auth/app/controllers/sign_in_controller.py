import json
from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest, JsonResponse
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.sign_in_dto import SignInDto, SignInDtoForm


class SignInController(BaseController):

    def __init__(self, sign_in_usecase: BaseUseCase) -> None:
        super().__init__()
        self.sign_in_usecase = sign_in_usecase

    def convert_to_form(self, request: HttpRequest) -> dict:
        return SignInDtoForm(json.loads(request.body))

    def convert_to_dto(self, data: dict) -> SignInDto:
        return SignInDto(email=data.get("email"), password=data.get("password"))

    async def execute_post(self, dto: SignInDto) -> JsonResponse:
        return await self.sign_in_usecase.execute(dto)
