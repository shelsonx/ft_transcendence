from functools import wraps
from ..exceptions.unauthorized_exception import UnauthorizedException
from ..services.jwt_service import JWTService
from django.http import JsonResponse
from ..entities.api_data_response import ApiDataResponse


class ProtectedRoute:
    def __init__(self, roles=[], func=None):
        self.roles = roles
        self.func = func

    def unauthorized(self, message: str = "Unauthorized"):
        api_data_response = ApiDataResponse(
            message=message,
            data=None,
            is_success=False
        ).to_dict()
        return JsonResponse(data=api_data_response, status=401, safe=False)

    def __call__(self, f):
        @wraps(f)
        async def decorated(*args, **kwargs):
            token = None
            try:
                request = args[1]
                if 'authorization' in request.headers:
                    auth_type, token = request.headers['authorization'].split(' ')
                    if auth_type != 'Bearer':
                        return self.unauthorized("Invalid token type - Bearer token required.")
                if not token:
                    return self.unauthorized("Token is missing")
                jwt_service = JWTService()
                try:
                    data = jwt_service.verify_token(token)
                    request.current_user = data
                    if self.func:
                        self.func(*args, **kwargs)
                except UnauthorizedException as e:
                    return self.unauthorized(message=e.message)
            except Exception as e:
                return self.unauthorized()        
            return await f(*args, **kwargs)
        return decorated
