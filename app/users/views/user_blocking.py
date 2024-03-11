from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..exception.exception import UserDoesNotExistException, InvalidUUIDException, InvalidFieldException
from ..models.models import User
from .user_info import UserInfoView

@method_decorator(csrf_exempt, name='dispatch')
class UserBlockingView(View):
    
    def get(self, request, user_id):
        """
        Get the users that the user with the given user_id has blocked.

        Args:
            user_id (str): The user_id to get the blocked users of

        Returns:
            JsonResponse: A JSON response containing the blocked users of the user with the given user_id

        Raises:
            UserDoesNotExistException: If the user with the given user_id does not exist
        """
        try:
            user = UserInfoView().get_user(user_id)
            blocked_users = user.blocked_users.all()
            blocked_users_json = [blocked_user.as_json() for blocked_user in blocked_users]
            return JsonResponse({'status': 'success', 'blocked_users': blocked_users_json, 'status_code': 200}, status=200)
        except UserDoesNotExistException as e:
            return JsonResponse(e.to_dict(), status=e.status_code)

    def post(self, request, user_id, blocked_id):
        """
        Add a user to the blocked users of a user.

        Args:
            user_id (str): The user_id to add the blocked user to
            blocked_id (str): The blocked_id to add to the user

        Returns:
            JsonResponse: A JSON response containing the status of the request

        Raises:
            UserDoesNotExistException: If the user with the given user_id or the blocked user with the given blocked_id does not exist
            InvalidUUIDException: If the user_id or blocked_id is not a valid UUID
        """
        try:
            user = UserInfoView().get_user(user_id)
            blocked = UserInfoView().get_user(blocked_id)
            user.blocked_users.add(blocked)
            return JsonResponse({'status': 'success', 'message': 'Blocked user added successfully', 'status_code': 200}, status=200)
        except UserDoesNotExistException as e:
            return JsonResponse(e.to_dict(), status=e.status_code)
        except InvalidUUIDException as e:
            return JsonResponse(e.to_dict(), status=e.status_code)
    
    def delete(self, request, user_id, blocked_id):
        """
        Remove a user from the blocked users of a user.

        Args:
            user_id (str): The user_id to remove the blocked user from
            blocked_id (str): The blocked_id to remove from the user

        Returns:
            JsonResponse: A JSON response containing the status of the request

        Raises:
            UserDoesNotExistException: If the user with the given user_id or the blocked user with the given blocked_id does not exist
            InvalidUUIDException: If the user_id or blocked_id is not a valid UUID
        """

        try:
            user = UserInfoView().get_user(user_id)
            blocked = UserInfoView().get_user(blocked_id)
            user.blocked_users.remove(blocked)
            return JsonResponse({'status': 'success', 'message': 'Blocked user removed successfully', 'status_code': 200}, status=200)
        except UserDoesNotExistException as e:
            return JsonResponse(e.to_dict(), status=e.status_code)
        except InvalidUUIDException as e:
            return JsonResponse(e.to_dict(), status=e.status_code)