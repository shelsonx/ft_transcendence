from abc import ABC, abstractmethod
from django.http import HttpRequest, JsonResponse
from ...exceptions.validation_error_exception import ValidationErrorException
from ...entities.api_data_response import ApiDataResponse
from ...exceptions.base_api_exception import BaseApiException
from django import forms
from ...utils.to_json_response import to_json_response
class BaseController(ABC):

  def __init__(self) -> None:
    super().__init__()

  @abstractmethod
  def convert_to_dto(self, data: dict) -> object:
    pass

  @abstractmethod
  def convert_to_form(self, request: HttpRequest) -> forms.Form:
    pass

  async def execute_get(self) -> object:
    raise NotImplementedError()
  
  async def execute_post(self, dto: object) -> object:
    raise NotImplementedError()

  async def execute_put(self, id: str, dto: object) -> object:
    raise NotImplementedError()
  
  async def execute_delete(self, id: str) -> object:
    raise NotImplementedError()
  
  async def handle_get(self, request: HttpRequest) -> JsonResponse:
    try:
      data = await self.execute_get()
      return self.to_json_response(data=ApiDataResponse(data=data))
    except BaseApiException as e:
        return self.to_json_response(data=ApiDataResponse(message=e.message, is_success=False), status=e.status_code)
    except Exception as e:
        return self.to_json_response(data=ApiDataResponse(message=str(e), is_success=False), status=500)  
    

  async def handle_post(self, request: HttpRequest) -> JsonResponse:
        try:
            form = self.convert_to_form(request)
            if not form.is_valid():
                raise ValidationErrorException(message=form.errors)
            dict_form = form.cleaned_data
            dto = self.convert_to_dto(dict_form)
            data = await self.execute_post(dto)
            return self.to_json_response(data=ApiDataResponse(data=data))
        except BaseApiException as e:
            return self.to_json_response(data=ApiDataResponse(message=e.message, is_success=False), status=e.status_code)
        except Exception as e:
            return self.to_json_response(data=ApiDataResponse(message=str(e), is_success=False), status=500)
        
  async def handle_put(self, request: HttpRequest, id: str) -> JsonResponse:
        try:
            form = self.convert_to_form(request)
            if not form.is_valid():
                raise ValidationErrorException(message=form.errors)
            dict_form = form.cleaned_data
            dto = self.convert_to_dto(dict_form)
            data = await self.execute_put(id, dto)
            return self.to_json_response(data=ApiDataResponse(data=data))
        except BaseApiException as e:
            return self.to_json_response(data=ApiDataResponse(message=e.message, is_success=False), status=e.status_code)
        except Exception as e:
            return self.to_json_response(data=ApiDataResponse(message=str(e), is_success=False), status=500)


  async def handle_delete(self, request: HttpRequest, id: str) -> JsonResponse:
        try:
            data = await self.execute_delete(id)
            return self.to_json_response(data=ApiDataResponse(data=data))
        except BaseApiException as e:
            return self.to_json_response(data=ApiDataResponse(message=e.message, is_success=False), status=e.status_code)
        except Exception as e:
            return self.to_json_response(data=ApiDataResponse(message=str(e), is_success=False), status=500)

  def to_json_response(self, data: ApiDataResponse, status=200) -> JsonResponse:
    return to_json_response(data, status)
