
from ..utils.to_json_response import to_json_response
from ..exceptions.base_api_exception import BaseApiException
from django.core.exceptions import ValidationError
from ..entities.api_data_response import ApiDataResponse

class ErrorHandlerMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ValidationError):
           return to_json_response(data=ApiDataResponse(message=exception.message_dict, is_success=False), status=400)
        if isinstance(exception, BaseApiException):
            return to_json_response(data=ApiDataResponse(message=exception.message, is_success=False), status=exception.status_code)
        return to_json_response(data=ApiDataResponse(message=str(exception), is_success=False), status=500)
