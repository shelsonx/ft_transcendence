# python std library
import uuid
from http import HTTPStatus

# Django
from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

# Local Folder
from .decorators import logged_permission
from .models import User
from .forms import UserForm


# TODO: SHEELA - check to remove this, csrf is important
@method_decorator(csrf_exempt, name="dispatch")
class UserView(generic.View):
    form_class = UserForm

    # talvez use a get para o Shelson, se ele precisar pedir em algum momento
    # def get(self, request: HttpRequest, pk: uuid) -> HttpResponse:
    #     print(request.path)
    #     if request.path == reverse_lazy("user:user_add"):
    #         return HttpResponseNotAllowed(permitted_methods=["POST"])

    # TODO: SHEELA - protect route to only gateway
    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        user = form.save()
        print("User created: ", user)
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    @logged_permission()
    def patch(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        # TODO: SHEELA - protect route
        user = User.objects.filter(pk=pk).first()
        form = self.form_class(request.POST, instance=user)
        if not form.is_valid():
            return HttpResponseBadRequest

        user = form.save()
        print("User deleted: ", user)
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    # TODO: SHEELA - protect route to only gateway
    def delete(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        # TODO: SHEELA - protect route
        user = get_object_or_404(User, pk=pk)
        user.delete()
        print("User deleted: ", user)
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
