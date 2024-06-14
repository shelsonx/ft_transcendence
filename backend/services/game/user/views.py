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
from user.decorators import JWTAuthentication
from common.models import json_response
from common.validators import is_valid_uuid4

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

    @JWTAuthentication(validate_user=False)
    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body)
        id = data.get("id")

        if id is None:
            return json_response.bad_request(msg="Missing user reference id")
        if not is_valid_uuid4(id):
            return json_response.bad_request(msg="Invalid user id format")
        if id != request.user_id:
            return json_response.bad_request(msg="Data mismatch")

        user = User.objects.filter(id=id)
        if user.exists():
            return json_response.bad_request(msg="User already registered")

        self.form = self.form_class(data, instance=User(id=id))
        if not self.form.is_valid():
            return json_response.bad_request(
                data=self.get_form_errors(), msg="Invalid data"
            )

        user: User = self.form.save()
        return json_response.success(msg="User created", status=HTTPStatus.CREATED)

    @JWTAuthentication()
    def patch(self, request: HttpRequest, pk: uuid) -> JsonResponse:
        user = User.objects.filter(pk=pk).first()
        if not user:
            return json_response.not_found(
                msg="User not found. Register it with POST method."
            )
        if request.user != user:
            return json_response.forbidden()

        data = json.loads(request.body)
        self.form = self.form_class(data, instance=user)
        if not self.form.is_valid():
            return json_response.bad_request(
                data=self.get_form_errors(), msg="Invalid data"
            )

        user: User = self.form.save()
        return json_response.success(msg="User updated")

    @JWTAuthentication()
    def delete(self, request: HttpRequest, pk: uuid) -> JsonResponse:
        user = User.objects.filter(pk=pk).first()
        if not user:
            return json_response.not_found()
        if request.user != user:
            return json_response.forbidden()

        user.delete()
        user = User.objects.filter(pk=pk).first()
        if user:
            return json_response.error(msg="User wasn't deleted")

        return json_response.success(msg="User deleted")

    def get_form_errors(self) -> dict:
        errors = {}
        for error, msg in self.form.errors.items():
            errors[error] = msg
        return errors
