# python std library
from http import HTTPStatus

# django
from django.http import JsonResponse


def success_json_response(
    data: dict = {}, msg: str = None, status: int = HTTPStatus.OK
) -> JsonResponse:
    data = {
        "data": data,
        "message": msg,
        "is_success": True,
    }
    return JsonResponse(data, status=status)


def error_json_response(
    data: dict = {}, msg: str = None, status: int = HTTPStatus.INTERNAL_SERVER_ERROR
) -> JsonResponse:
    data = {
        "data": data,
        "message": msg,
        "is_success": False,
    }
    return JsonResponse(data, status=status)


def json_bad_request(data: dict = {}, msg: str = None) -> JsonResponse:
    return error_json_response(data=data, msg=msg, status=HTTPStatus.BAD_REQUEST)


def json_not_found(data: dict = {}, msg: str = None) -> JsonResponse:
    return error_json_response(data=data, msg=msg, status=HTTPStatus.NOT_FOUND)
