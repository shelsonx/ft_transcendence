from django.urls import path
from .views.auth_view import AuthView
from .router.auth.auth_router import AuthRouter
from .services.http_client import HttpClient
from .router.api_urls import ApiUrls

http_client = HttpClient(ApiUrls.AUTH)
auth_router = AuthRouter(
  http_client=http_client
)

urlpatterns = [
    path("auth/<path:slug>", AuthView.as_view(
        auth_router=auth_router
    )),
]
