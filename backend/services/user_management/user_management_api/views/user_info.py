import uuid
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http.multipartparser import MultiPartParser, MultiPartParserError
from django.views.decorators.csrf import csrf_exempt

from user_management_api.exception.exception \
    import UserDoesNotExistException, InvalidUUIDException, \
    InvalidFormDataException
from user_management_api.forms import UserForm
from user_management_api.models.models import User
import json


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
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserDoesNotExistException

    def delete(self, request, user_id):
        user = self.get_user(user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'User deleted successfully', 'status_code': 200}, status=200)

    def post(self, request):
        form = UserForm(json.loads(request.body.decode('utf-8')))
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'User created successfully', 'status_code': 201}, status=201)
        else:
            raise InvalidFormDataException

    def get(self, request, user_id=None):
        if user_id:
            user = self.get_user(user_id)
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'status': 'success', 'user': user.as_json()}, status=200)
            return render(request, 'user_profile.html', {'user': user.as_json()})
        else:
            users = User.objects.all()
            users_json = [user.as_json() for user in users]
            return JsonResponse({'status': 'success', 'users': users_json}, status=200, safe=False)

    def patch(self, request, user_id):
        
        user = User.objects.get(id=user_id)

        if request.headers.get('Content-Type', '').startswith('multipart/form-data'):
            try:
                request.upload_handlers.insert(0, TemporaryFileUploadHandler(request))
                parser = MultiPartParser(request.META, request, request.upload_handlers)
                data, files = parser.parse()

                form = UserForm(data, files, instance=user)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'status': 'success', 'message': 'User updated successfully', 'status_code': 200}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid form data', 'status_code': 400, 'errors': form.errors}, status=400)
            except MultiPartParserError as e:
                return JsonResponse({'status': 'error', 'message': f'Error parsing multipart data: {e}', 'status_code': 400}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Content-Type must be multipart/form-data', 'status_code': 400}, status=400)
