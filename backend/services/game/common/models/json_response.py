# python std library
from http import HTTPStatus

# django
from django.http import JsonResponse


def success(
    data: dict = {}, msg: str = None, status: int = HTTPStatus.OK
) -> JsonResponse:
    data = {
        "data": data,
        "message": msg,
        "is_success": True,
    }
    return JsonResponse(data, status=status)


def error(
    data: dict = {}, msg: str = None, status: int = HTTPStatus.INTERNAL_SERVER_ERROR
) -> JsonResponse:
    data = {
        "data": data,
        "message": msg,
        "is_success": False,
    }
    return JsonResponse(data, status=status)


def bad_request(data: dict = {}, msg: str = "Bad Request") -> JsonResponse:
    return error(data=data, msg=msg, status=HTTPStatus.BAD_REQUEST)

def not_found(data: dict = {}, msg: str = "Not found") -> JsonResponse:
    return error(data=data, msg=msg, status=HTTPStatus.NOT_FOUND)

def forbidden(data: dict = {}, msg: str = "Permission Denied") -> JsonResponse:
    return error(data=data, msg=msg, status=HTTPStatus.FORBIDDEN)
