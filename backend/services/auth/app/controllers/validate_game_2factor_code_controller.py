from ..exceptions.two_factor_exception import TwoFactorCodeException
from ..entities.api_data_response import ApiDataResponse
from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest, JsonResponse, QueryDict
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.validate_game_2factor_code_dto import (
    ValidateGame2FactorCodeDto,
    ValidateGame2FactorCodeForm,
)
import json


class ValidateGame2FactorCodeController(BaseController):

    def __init__(
        self,
        validate_game_2factor_code_usecase: BaseUseCase,
        send_game_2factor_code_usecase: BaseUseCase,
    ) -> None:
        super().__init__()
        self.validate_game_2factor_code_usecase = validate_game_2factor_code_usecase
        self.send_game_2factor_code_usecase = send_game_2factor_code_usecase

    def convert_to_form(self, request: HttpRequest) -> dict:
        return ValidateGame2FactorCodeForm(json.loads(request.body))

    def convert_to_dto(self, data: dict) -> ValidateGame2FactorCodeDto:
        return ValidateGame2FactorCodeDto(
            user_receiver_id=data["user_receiver_id"],
            user_requester_id=data["user_requester_id"],
            game_type=data["game_type"],
            game_id=data["game_id"],
        )

    async def execute_post(self, dto: ValidateGame2FactorCodeDto) -> JsonResponse:
        return await self.validate_game_2factor_code_usecase.execute(dto)

    async def execute_put(self, dto: ValidateGame2FactorCodeDto) -> ValidateGame2FactorCodeDto:
        return await self.send_game_2factor_code_usecase.execute(dto)

    async def handle_put(self, request: HttpRequest) -> JsonResponse:
        forms = ValidateGame2FactorCodeForm(json.loads(request.body))
        dto = self.validate_form(forms)
        if not dto.two_factor_code:
            raise TwoFactorCodeException()
        data = await self.execute_put(dto)
        return self.to_json_response(data=ApiDataResponse(data=data))
