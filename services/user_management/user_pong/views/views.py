from http import HTTPStatus
from django.shortcuts import render
from ..models import UserPong

from django.http import HttpRequest, HttpResponse

from django.views import generic

# Create your views here.

def get_test(request: HttpRequest) -> HttpResponse:
    user = UserPong.objects.all().first()
    template = "user_pong/test.html"
    context = {
        "name": None,
    }
    return render(request, template, context)


class ViewTest(generic.FormView):
    template = "user_pong/test.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        for k, v in request.GET.items():
            print(k, v)
        user = UserPong.objects.all().first()
        context = {
            "name": user.name,
        }
        return render(request, self.template, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        request.POST()
        pass

    def patch(self, request: HttpRequest) -> HttpResponse:
        pass
