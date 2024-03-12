from django.http import JsonResponse
from ..exception.exception import UserDoesNotExistException, InvalidUUIDException, \
    InvalidFieldException, InvalidFormDataException, InvalidJSONDataException, \
    UserManagementException, FriendshipAlreadyExistsException

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, UserDoesNotExistException):
            return JsonResponse(exception.to_dict(), status=exception.status_code)
        elif isinstance(exception, InvalidUUIDException):
            return JsonResponse(exception.to_dict(), status=exception.status_code)
        elif isinstance(exception, InvalidFieldException):
            return JsonResponse(exception.to_dict(), status=exception.status_code)
        elif isinstance(exception, InvalidFormDataException):
            return JsonResponse(exception.to_dict(), status=exception.status_code)
        elif isinstance(exception, InvalidJSONDataException):
            return JsonResponse(exception.to_dict(), status=exception.status_code)
        elif isinstance(exception, UserManagementException):
            return JsonResponse(exception.to_dict(), status=exception.status_code)
        elif isinstance(exception, FriendshipAlreadyExistsException):
            return JsonResponse(exception.to_dict(), status=exception.status_code)
        else:
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred', 'status_code': 500}, status=500)