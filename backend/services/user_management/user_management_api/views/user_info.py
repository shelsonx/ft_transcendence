import os
import uuid
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http.multipartparser import MultiPartParser, MultiPartParserError
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from user_management_api.jwt.decorator import JWTAuthentication
from user_management_api.exception.exception import (
    UserDoesNotExistException,
    InvalidUUIDException,
    InvalidFormDataException
)
from user_management_api.forms import UserForm
from user_management_api.models.models import User
import json
from django.utils.translation import gettext as _


@method_decorator(csrf_exempt, name='dispatch')
class UserInfoView(View):
    """
    Handles user information operations.
    `get`: Retrieves the user information for the specified user.
    `post`: Creates a new user.
    `delete`: Deletes the specified user.
    `patch`: Updates the specified user according to the request body.
    """

    def is_valid_uuid(self, user_id):
        try:
            uuid.UUID(str(user_id), version=4)
            return True
        except ValueError:
            return False

    def get_user(self, user_id):
        if not self.is_valid_uuid(user_id):
            raise InvalidUUIDException
        try:
            return User.objects.get(user_uuid=user_id)
        except User.DoesNotExist:
            raise UserDoesNotExistException

    @JWTAuthentication()
    def delete(self, request, user_id):
        user_deleted_message = _('User deleted successfully')
        user = self.get_user(user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': user_deleted_message, 'status_code': 200}, status=200)

    def post(self, request):
        user_created_message = _('User created successfully')
        form = UserForm(json.loads(request.body.decode('utf-8')))
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': user_created_message, 'status_code': 201}, status=201)
        else:
            raise InvalidFormDataException

    @JWTAuthentication()
    def get(self, request, user_id=None):
        if user_id:
            user = self.get_user(user_id)
            return JsonResponse({'status': 'success', 'user': user.as_json()}, status=200)
        else:
            nickname = request.GET.get('nickname')
            name = request.GET.get('name')
            email = request.GET.get('email')
            status = request.GET.get('status')

            filters = Q()
            if nickname:
                filters &= Q(nickname__icontains=nickname)
            if name:
                filters &= Q(name__icontains=name)
            if email:
                filters &= Q(email__icontains=email)
            if status:
                filters &= Q(status=status)

            users = User.objects.filter(filters)
            users_json = [user.as_json() for user in users]
            return JsonResponse({'status': 'success', 'users': users_json}, status=200, safe=False)

    @JWTAuthentication()
    def patch(self, request, user_id):
        user_updated_message = _('User updated successfully')
        invalid_form_data_message = _('Invalid form data')
        multipart_form_data_message = _('Content-Type must be multipart/form-data')
        parser_error_message = _('Error parsing multipart data')
        user = User.objects.get(user_uuid=user_id)

        if request.headers.get('Content-Type', '').startswith('multipart/form-data'):
            try:
                request.upload_handlers.insert(0, TemporaryFileUploadHandler(request))
                parser = MultiPartParser(request.META, request, request.upload_handlers)
                data, files = parser.parse()

                form = UserForm(data, files, instance=user)
                if form.is_valid():
                    user = form.save(commit=False)

                    if 'avatar' in files:
                        avatar = files['avatar']
                        avatar_name = f'{data["avatar_name"]}'
                        user.avatar.save(avatar_name, avatar)

                    user.save()
                    return JsonResponse({'status': 'success', 'message': user_updated_message, 'status_code': 200}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': invalid_form_data_message, 'status_code': 400, 'errors': form.errors}, status=400)
            except MultiPartParserError as e:
                return JsonResponse({'status': 'error', 'message': parser_error_message, 'status_code': 400}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': multipart_form_data_message, 'status_code': 400}, status=400)
