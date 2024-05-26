# Python STD library
from functools import wraps
from http import HTTPStatus
from os import environ

# Django
from django.http import HttpResponse, JsonResponse

# Local Folder
from .exceptions import UnauthorizedException
from .services import JWTService


class JWTAuthenticationMiddleware:
    def __init__(self, roles=[], func=None, secret=None):
        self.roles = roles
        self.func = func
        self.secret = secret

    def unauthorized(self, message: str = "Unauthorized"):
        return HttpResponse(
            content=message,
            status=HTTPStatus.UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer token68"},
        )

    def __call__(self, f):
        @wraps(f)
        async def decorated(*args, **kwargs):
            token = None
            try:
                request = args[1]
                if "authorization" in request.headers:
                    auth_type, token = request.headers["authorization"].split(" ")
                    if auth_type != "Bearer":
                        return self.unauthorized(
                            "Invalid token type - Bearer token required."
                        )
                if not token:
                    return self.unauthorized("Token is missing")
                jwt_service = JWTService()
                try:
                    secret = (
                        environ.get("JWT_SECRET") if not self.secret else self.secret
                    )
                    data = jwt_service.verify_token(token, secret)
                    request.current_user = data
                    if self.func:
                        self.func(*args, **kwargs)
                except UnauthorizedException as e:
                    return self.unauthorized(message=e.message)
            except Exception as e:
                return self.unauthorized()
            return await f(*args, **kwargs)

        return decorated
