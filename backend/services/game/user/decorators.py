# Third Party
from http import HTTPStatus
from django.http import HttpRequest, HttpResponse


def logged_permission():
    """

    """

    def decorator(view_func):
        def wrapper(view_class, request: HttpRequest, *args, **kwargs):
            authorization = request.headers.get("authorization")
            if not authorization:
                return unauthorized()
            auth_type, token = authorization.split(" ")
            if auth_type != "Bearer":
                return unauthorized(
                    "Invalid token type - Bearer token required."
                )
            if not token:
                return unauthorized("Token is missing")

            return view_func(view_class, request, *args, **kwargs)

        return wrapper

    def unauthorized(message: str = "Unauthorized"):
        return HttpResponse(status=HTTPStatus.UNAUTHORIZED, content=message)

    return decorator
