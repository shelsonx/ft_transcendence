from abc import ABC, abstractmethod
from django.http import HttpRequest, JsonResponse


class BaseOAuth42Controller(ABC):

    @abstractmethod
    async def handle_callback(self, request: HttpRequest) -> JsonResponse:
        pass
