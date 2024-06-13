# Third Party
from functools import wraps
from http import HTTPStatus
from os import environ
from django.http import Http404, HttpRequest, HttpResponse

from common.exceptions import UnauthorizedException
from common.services import JWTService
from user.models import User


class JWTAuthentication:
    def __init__(self, roles=[], func=None, secret=None, validate_user=True):
        self.roles = roles
        self.func = func
        self.secret = secret
        self.validate_user = validate_user

    def unauthorized(self, message: str = "Unauthorized"):
        return HttpResponse(
            content=message,
            status=HTTPStatus.UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer token68"},
        )

    def __call__(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            try:
                request: HttpRequest = args[1]

                if "authorization" in request.headers:
                    auth_type, token = request.headers["authorization"].split(" ")
                    if auth_type != "Bearer":
                        return self.unauthorized(
                            "Invalid token type - Bearer token required."
                        )

                if not token:
                    return self.unauthorized("Token is missing")

                try:
                    secret = (
                        environ.get("JWT_SECRET") if not self.secret else self.secret
                    )

                    jwt_service = JWTService()
                    data = jwt_service.verify_token(token, secret)
                    request.user = User.get_object(pk=data.sub)
                    if not request.user and self.validate_user:
                        return self.unauthorized("user not registered")
                    if not self.validate_user:
                        request.user_id = data.sub

                    if self.func:
                        self.func(*args, **kwargs)
                except UnauthorizedException as e:
                    return self.unauthorized(message=e.message)
            except Exception:
                return self.unauthorized()
            return f(*args, **kwargs)

        return decorated
