from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .user_info import UserInfoView

from ..exception.exception import MissingParameterException, UserDoesNotExistException
from ..models.models import User

@method_decorator(csrf_exempt, name='dispatch')
class UserFriendshipView(View):

    def get(self, request, user_id):
        """
        Get the friends of a user.

        Args:
            user_id (str): The user_id to get the friends of

        Returns:
            JsonResponse: A JSON response containing the friends of the user with the given user_id

        Raises:
            UserDoesNotExistException: If the user with the given user_id does not exist
        """
        try:
            user = UserInfoView().get_user(user_id)
            friends = user.friends.all()
            friends_json = [friend.as_json() for friend in friends]
            return JsonResponse({'status': 'success', 'friends': friends_json}, status=200, safe=False)
        except UserDoesNotExistException:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'}, status=404)

    def post(self, request, user_id, friend_id=None):
        """
        Add a friend to a user.

        Args:
            user_id (str): The user_id to add the friend to
            friend_id (str): The friend_id to add to the user

        Returns:
            JsonResponse: A JSON response containing the status of the request

        Raises:
            UserDoesNotExistException: If the user with the given user_id or the friend with the given friend_id does not exist
            MissingParameterException: If the friend_id is not provided
        """
        try:
            if friend_id is None:
                raise MissingParameterException('friend_id')
            user = UserInfoView().get_user(user_id)
            friend = UserInfoView().get_user(friend_id)
            user.friends.add(friend)
            return JsonResponse({'status': 'success', 'message': 'Friend added successfully'}, status=200)
        except UserDoesNotExistException:
            return JsonResponse({'status': 'error', 'message': 'User or friend does not exist'}, status=404)
        except MissingParameterException as e:
            return JsonResponse({'status': 'error', 'message': f'Missing parameter: {e}'}, status=400)

    def delete(self, request, user_id, friend_id=None):
        """
        Remove a friend from a user.

        Args:
            user_id (str): The user_id to remove the friend from
            friend_id (str): The friend_id to remove from the user

        Returns:
            JsonResponse: A JSON response containing the status of the request

        Raises:
            UserDoesNotExistException: If the user with the given user_id or the friend with the given friend_id does not exist
            MissingParameterException: If the friend_id is not provided
        """

        try:
            if friend_id is None:
                raise MissingParameterException('friend_id')
            user = UserInfoView().get_user(user_id)
            friend = UserInfoView().get_user(friend_id)
            user.friends.remove(friend)
            return JsonResponse({'status': 'success', 'message': 'Friend removed successfully'}, status=200)
        except UserDoesNotExistException:
            return JsonResponse({'status': 'error', 'message': 'User or friend does not exist'}, status=404)
        except MissingParameterException as e:
            return JsonResponse({'status': 'error', 'message': f'Missing parameter: {e}'}, status=400)

