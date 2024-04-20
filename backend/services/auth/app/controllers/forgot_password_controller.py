import json
from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest, JsonResponse
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.forgot_password_dto import ForgotPasswordDto, ForgotPasswordDtoForm


class ForgotPasswordController(BaseController):

    def __init__(self, forgot_password_usecase: BaseUseCase) -> None:
        super().__init__()
        self.forgot_password_usecase = forgot_password_usecase

    def convert_to_form(self, request: HttpRequest) -> dict:
        return ForgotPasswordDtoForm(json.loads(request.body))

    def convert_to_dto(self, data: dict) -> ForgotPasswordDto:
        return ForgotPasswordDto(email=data.get("email"), two_factor_code=data.get("two_factor_code"), password=data.get("password"))

    async def execute_post(self, dto: ForgotPasswordDto) -> JsonResponse:
        return await self.forgot_password_usecase.execute(dto)
