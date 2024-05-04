
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

    def prepare_query_strings(self, path: str, request: HttpRequest):
        query_str = ""
        count = len(request.GET.keys())
        for key, value in request.GET.items():
            query_str += f"{key}={value}"
            if count > 1:
                query_str += "&"
            count -= 1
        if query_str:
            path += f"?{query_str}"
        return path

    def post(self, request: HttpRequest, slug, *args, **kwargs) -> JsonResponse:
        path = self.prepare_query_strings(slug, request)
        return self.auth_router.route("POST", f"/{path}", request, *args, **kwargs)

    def get(self, request: HttpRequest, slug, *args, **kwargs) -> JsonResponse:
        path = self.prepare_query_strings(slug, request)
        return self.auth_router.route("GET", f"/{path}", request, *args, **kwargs)

    def put(self, request: HttpRequest, slug, *args, **kwargs) -> JsonResponse:
       path = self.prepare_query_strings(slug, request)
       return self.auth_router.route("PUT", f"/{path}", request, *args, **kwargs)

    def delete(self, request: HttpRequest, slug, *args, **kwargs) -> JsonResponse:
       path = self.prepare_query_strings(slug, request)
       return self.auth_router.route("DELETE", f"/{path}", request, *args, **kwargs)

