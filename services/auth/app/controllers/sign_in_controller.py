
from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest, HttpResponse,JsonResponse
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.sign_in_dto import SignInDto
import json
from typing import Dict
from ..entities.fields import Field
from ..exceptions.BaseApiException import BaseApiException
from ..entities.api_data_response import ApiDataResponse
from django.core.validators import validate_email

class SignInController(BaseController):


  def __init__(self, sign_in_usecase: BaseUseCase) -> None:
    super().__init__(
        fields={
        "email": Field(name='email', is_required=True, field_type=str, validators=[validate_email]),
        "password": Field(name='password', is_required=True, field_type=str),
      }
    )
    self.sign_in_usecase = sign_in_usecase
    self.dto: SignInDto = {}

  def convert_to_dto(self, data: dict) -> SignInDto:
    return SignInDto(email=data.get('email'), password=data.get('password'))

  async def execute(self, dto: SignInDto) -> JsonResponse:
   return await self.sign_in_usecase.execute(dto)