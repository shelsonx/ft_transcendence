
from django.views import View
from django.http import HttpRequest, JsonResponse
from ..interfaces.router.router import IRouter
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name="dispatch")
class AuthView(View):
    auth_router: IRouter = None 

    def __init__(self, auth_router: IRouter) -> None:
      self.auth_router = auth_router

    def post(self, request: HttpRequest, slug, *args, **kwargs) -> JsonResponse:
        return self.auth_router.route("POST", f"/{slug}", request, *args, **kwargs)
    
    def get(self, request: HttpRequest, slug, *args, **kwargs) -> JsonResponse:
        return self.auth_router.route("GET", f"/{slug}", request, *args, **kwargs)
    
    def put(self, request: HttpRequest, slug, *args, **kwargs) -> JsonResponse:
       return self.auth_router.route("PUT", f"/{slug}", request, *args, **kwargs)

    def delete(self, request: HttpRequest, slug, *args, **kwargs) -> JsonResponse:
       return self.auth_router.route("DELETE", f"/{slug}", request, *args, **kwargs)

