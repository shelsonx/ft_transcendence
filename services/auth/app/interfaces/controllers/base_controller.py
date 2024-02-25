from abc import ABC, abstractmethod
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from typing import List, Dict
from ...exceptions.ValidationErrorException import ValidationErrorException
from ...entities.fields import Field
from copy import deepcopy
from ...entities.api_data_response import ApiDataResponse
from ...exceptions.BaseApiException import BaseApiException

class BaseController(ABC):

  def __init__(self, fields: Dict[str, Field] = {}) -> None:
    super().__init__()
    self.fields: Dict[str, Field] = fields
    self.errors: Dict[str, List[str]] = {}
    self.dto: object = None

  @abstractmethod
  def convert_to_dto(self, data: dict) -> object:
    pass
  
  @abstractmethod
  async def execute(self, dto: object) -> object:
    pass

  async def handle(self, request: HttpRequest) -> JsonResponse:
    try:
      dto = self.validate_parse_dto(request)
      data = await self.execute(dto)
      return self.to_json_response(data=ApiDataResponse(data=data))
    except BaseApiException as e:
      return self.to_json_response(data=ApiDataResponse(message=e.message, is_success=False), status=e.status_code)
    except Exception as e:
      return self.to_json_response(data=ApiDataResponse(message=e.message, is_success=False), status=500)
    finally:
      self.errors = {}

  def validate_parse_dto(self, request: HttpRequest) -> object:
    dto = self.post_data_to_dto(request)
    if self.validate(dto):
      return dto
    raise ValidationErrorException(message=self.errors)

  def validate(self, dto: object) -> bool:
    if dto is None:
      return False
    for key in dto.__dict__.keys():
      value = getattr(dto, key)
      field = self.fields[key]
      if value is None and field.is_required:
        self.add_error(key, "cannot be null")
      if isinstance(value, str) and value == '':
        self.add_error(key, "cannot be empty")

      for validator in field.validators:
          try:
            validator(value)
          except Exception as e:
            self.add_error(key, str(e))

      if not isinstance(value, field.field_type):
        self.add_error(key, f"must be a {field.field_type} type'")
    if len(self.errors.keys()) > 0:
      return False
    return True
  
  ## def common_validations(self, dto: object) -> bool:

  def post_data_to_dto(self, request: HttpRequest) -> object:
    dto = None
    current_dict = {}
    for key, value in self.fields.items():
      post_item = request.POST.get(value.name)
      current_dict[value.name] =  post_item
    self.dto = self.convert_to_dto(current_dict)
    dto = deepcopy(self.dto)
    return dto
  
  def add_error(self, field: str, message: str) -> None:
    if field not in self.errors:
      self.errors[field] = []
    self.errors[field].append(message)

  def to_json_response(self, data: ApiDataResponse, status=200) -> HttpResponse:
    return JsonResponse(status=status, data=data.to_dict(), safe=False)
