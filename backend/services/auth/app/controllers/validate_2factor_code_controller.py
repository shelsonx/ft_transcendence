from ..exceptions.two_factor_exception import TwoFactorCodeException
from ..entities.api_data_response import ApiDataResponse
from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest, JsonResponse, QueryDict
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.validate_2factor_code_dto import (
    Validate2FactorCodeDto,
    Validate2FactorCodeForm,
)
import json

class Validate2FactorCodeController(BaseController):

    def __init__(
        self,
        validate_2factor_code_usecase: BaseUseCase,
        send_2factor_code_usecase: BaseUseCase,
    ) -> None:
        super().__init__()
        self.validate_2factor_code_usecase = validate_2factor_code_usecase
        self.send_2factor_code_usecase = send_2factor_code_usecase

    def convert_to_form(self, request: HttpRequest) -> dict:
        return Validate2FactorCodeForm(json.loads(request.body))

    def convert_to_dto(self, data: dict) -> Validate2FactorCodeDto:
        return Validate2FactorCodeDto(
            email=data.get("email"), two_factor_code=data.get("two_factor_code")
        )

    async def execute_post(self, dto: Validate2FactorCodeDto) -> JsonResponse:
        return await self.send_2factor_code_usecase.execute(dto)

    async def execute_put(self, dto: object) -> object:
        return await self.validate_2factor_code_usecase.execute(dto)

    async def handle_put(self, request: HttpRequest) -> JsonResponse:
        forms = Validate2FactorCodeForm(json.loads(request.body))
        dto = self.validate_form(forms)
        if not dto.two_factor_code:
            raise TwoFactorCodeException()
        data = await self.execute_put(dto)
        return self.to_json_response(data=ApiDataResponse(data=data))
