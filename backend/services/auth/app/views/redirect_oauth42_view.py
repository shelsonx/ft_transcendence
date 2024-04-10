from typing import Any
from django.http import HttpRequest, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views import View

from ..utils.build_oauth42_url import build_oauth42_url
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect


@method_decorator(csrf_exempt, name="dispatch")
class RedirectOAuth42View(View):

    async def get(
        self, request: HttpRequest
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        url_42 = build_oauth42_url()
        return redirect(url_42)
