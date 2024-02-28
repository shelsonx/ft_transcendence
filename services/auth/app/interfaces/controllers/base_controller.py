from abc import ABC, abstractmethod
from django.http import HttpRequest, JsonResponse
from ...exceptions.ValidationErrorException import ValidationErrorException
from ...entities.api_data_response import ApiDataResponse
from ...exceptions.BaseApiException import BaseApiException
from django import forms

class BaseController(ABC):

  def __init__(self) -> None:
    super().__init__()

  @abstractmethod
  def convert_to_dto(self, data: dict) -> object:
    pass

  @abstractmethod
  def convert_to_form(self, request: HttpRequest) -> forms.Form:
    pass
  
  @abstractmethod
  async def execute(self, dto: object) -> object:
    pass

  async def handle(self, request: HttpRequest) -> JsonResponse:
        try:
            form = self.convert_to_form(request)
            if not form.is_valid():
                raise ValidationErrorException(message=form.errors)
            dict_form = form.cleaned_data
            dto = self.convert_to_dto(dict_form)
            data = await self.execute(dto)
            return self.to_json_response(data=ApiDataResponse(data=data))
        except BaseApiException as e:
            return self.to_json_response(data=ApiDataResponse(message=e.message, is_success=False), status=e.status_code)
        except Exception as e:
            return self.to_json_response(data=ApiDataResponse(message=str(e), is_success=False), status=500)

  def to_json_response(self, data: ApiDataResponse, status=200) -> JsonResponse:
    return JsonResponse(status=status, data=data.to_dict(), safe=False)
