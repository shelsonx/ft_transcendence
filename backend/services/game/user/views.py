# python std library
from http import HTTPStatus
import json
import uuid

# Django
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

# First Party
from common.models import (
    error_json_response,
    json_bad_request,
    json_not_found,
    success_json_response,
)
from common.decorators import logged_permission

# Local Folder
from .models import User
from .forms import UserForm


@method_decorator(csrf_exempt, name="dispatch")
class UserView(generic.View):
    form_class = UserForm

    # talvez use a get para o Shelson, se ele precisar pedir em algum momento
    # def get(self, request: HttpRequest, pk: uuid) -> JsonResponse:
    #     print(request.path)
    #     if request.path == reverse_lazy("user:user_add"):
    #         return HttpResponseNotAllowed(permitted_methods=["POST"])

    # TODO: SHEELA - protect route to only gateway
    def post(self, request: HttpRequest) -> JsonResponse:
        # TODO: SHEELA - protect route
        data = json.loads(request.body)
        id = data.get("id")  # TODO: validate uuid

        user = User.objects.filter(id=id)
        if user.exists():
            return json_bad_request(msg="User already registered")

        if id is None:
            return json_bad_request(msg="Missing user reference id")

        self.form = self.form_class(data, User(id=id))
        if not self.form.is_valid():
            return json_bad_request(data=self.get_form_errors(), msg="Invalid data")

        user: User = self.form.save(commit=False)
        user.id = id
        user.save()

        return success_json_response(msg="User created", status=HTTPStatus.CREATED)

    # @logged_permission()
    def patch(self, request: HttpRequest, pk: uuid) -> JsonResponse:
        # TODO: SHEELA - protect route - should be the same user in the JWT?
        user = User.objects.filter(pk=pk).first()
        if not user:
            return json_not_found(msg="User not found. Register it with POST method.")

        data = json.loads(request.body)
        self.form = self.form_class(data, instance=user)
        if not self.form.is_valid():
            return json_bad_request(data=self.get_form_errors(), msg="Invalid data")

        user: User = self.form.save()
        return success_json_response(msg="User updated")

    # TODO: SHEELA - protect route to only gateway
    def delete(self, request: HttpRequest, pk: uuid) -> JsonResponse:
        # TODO: SHEELA - protect route - should be the same user in the JWT?
        user = User.objects.filter(pk=pk).first()
        if not user:
            return json_not_found(msg="User not found")

        user.delete()
        user = User.objects.filter(pk=pk).first()
        if user:
            return error_json_response(msg="User wasn't deleted")

        return success_json_response(msg="User deleted")

    def get_form_errors(self) -> dict:
        errors = {}
        for error, msg in self.form.errors.items():
            errors[error] = msg
        return errors
