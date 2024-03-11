import uuid
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..exception.exception import UserDoesNotExistException, InvalidUUIDException, InvalidFieldException
from ..forms import UserForm
from ..models.models import User
import json


@method_decorator(csrf_exempt, name='dispatch')
class UserInfoView(View):

    def is_valid_uuid(self, user_id):
        """
        Check if the user_id is a valid UUID

        Args:
            user_id (str): The user_id to check

        Returns:

        Raises:
            InvalidUUIDException: If the user_id is not a valid UUID
        """
        if isinstance(user_id, uuid.UUID):
            return True
        try:
            uuid.UUID(str(user_id), version=4)
            return True
        except ValueError:
            raise InvalidUUIDException

    def get_user(self, user_id):
        """
        Get the user with the given user_id

        Args:
            user_id (str): The user_id to get from the database

        Returns:
            User: The user instance with the given user_id

        Raises:
            UserDoesNotExistException: If the user with the given user_id does not exist
            InvalidUUIDException: If the user_id is not a valid UUID
        """
        self.is_valid_uuid(user_id)
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserDoesNotExistException


    def delete(self, request, user_id):
        """
        Delete the user with the given user_id

        Args:
            user_id (str): The user_id to delete from the database

        Returns:
            JsonResponse: The response to the request with the status and message of the operation result

        Raises:
            UserDoesNotExistException: If the user with the given user_id does not exist
            InvalidUUIDException: If the user_id is not a valid UUID
        """
        try:
            user = self.get_user(user_id)
            user.delete()
            return JsonResponse({'status': 'success', 'message': 'User deleted successfully'}, status=200)
        except UserDoesNotExistException:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
        except InvalidUUIDException:
            return JsonResponse({'status': 'error', 'message': 'Invalid user id'}, status=400)

    def post(self, request):
        """
        Create a new user with the given data

        Args:
            request (HttpRequest): The request object with the user data in the body as JSON

        Returns:
            JsonResponse: The response to the request with the status and message of the operation result

        Raises:
            UserDoesNotExistException: If the user with the given user_id does not exist
            InvalidUUIDException: If the user_id is not a valid UUID
            JSONDecodeError: If the request body is not a valid JSON
        """
        try:
            form = UserForm(json.loads(request.body.decode('utf-8')))
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'User created successfully'}, status=201)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def get(self, request, user_id=None):
        """
        Get the user with the given user_id or all users

        Args:
            user_id (str): The user_id to get from the database

        Returns:
            JsonResponse: The response to the request with the status and message of the operation result

        Raises:
            UserDoesNotExistException: If the user with the given user_id does not exist
            InvalidUUIDException: If the user_id is not a valid UUID
        """
        if user_id:
            try:
                user = self.get_user(user_id)
                return JsonResponse({'status': 'success', 'user': user.as_json()}, status=200)
            except InvalidUUIDException:
                return JsonResponse({'status': 'error', 'message': 'Invalid user id'}, status=400)
            except UserDoesNotExistException:
                return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
        else:
            users = User.objects.all()
            users_json = [user.as_json() for user in users]
            return JsonResponse({'status': 'success', 'users': users_json}, status=200, safe=False)

    def patch(self, request, user_id):
        """
        Update the user with the given user_id

        Args:
            request (HttpRequest): The request object with the user data in the body as JSON
            user_id (str): The user_id to update in the database

        Returns:
            JsonResponse: The response to the request with the status and message of the operation result

        Raises:
            UserDoesNotExistException: If the user with the given user_id does not exist
            InvalidUUIDException: If the user_id is not a valid UUID
            InvalidFieldException: If the request body has an invalid field
        """
        try:
            user = self.get_user(user_id)
            data = json.loads(request.body.decode('utf-8'))
            for field in ['username', 'status', 'avatar', 'nickname', 'two_factor_enabled', 'email']:
                if field in data:
                    setattr(user, field, data[field])
                else:
                    raise InvalidFieldException
            user.save()
            return JsonResponse({'status': 'success', 'message': 'User updated successfully'}, status=200)
        except InvalidFieldException:
            return JsonResponse({'status': 'error', 'message': 'Invalid field'}, status=400)
        except UserDoesNotExistException:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)
        except InvalidUUIDException:
            return JsonResponse({'status': 'error', 'message': 'Invalid user id'}, status=400)
