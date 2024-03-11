from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .user_info import UserInfoView

from ..exception.exception import MissingParameterException, UserDoesNotExistException, FriendshipAlreadyExistsException
from ..models.models import User

@method_decorator(csrf_exempt, name='dispatch')
class UserFriendshipView(View):
    """
    Handles adding and removing friends for users.
    `get`: Retrieves the list of friends for the specified user.
    `post`: Adds a friend for the specified user.
    `delete`: Removes a previously added friend for the specified user.
    """

    def get(self, request, user_id):
        user = UserInfoView().get_user(user_id)
        friends = user.friends.all()
        friends_json = [friend.as_json() for friend in friends]
        return JsonResponse({'status': 'success', 'friends': friends_json, 'status_code': 200}, status=200)

    def post(self, request, user_id, friend_id=None):
        if friend_id is None:
            raise MissingParameterException("friend_id")
        user = UserInfoView().get_user(user_id)
        friend = UserInfoView().get_user(friend_id)
        if friend in user.friends.all():
            raise FriendshipAlreadyExistsException
        user.friends.add(friend)
        return JsonResponse({'status': 'success', 'message': 'Friend added successfully', 'status_code': 200}, status=200)

    def delete(self, request, user_id, friend_id=None):
        if friend_id is None:
            raise MissingParameterException("friend_id")
        user = UserInfoView().get_user(user_id)
        friend = UserInfoView().get_user(friend_id)
        user.friends.remove(friend)
        return JsonResponse({'status': 'success', 'message': 'Friend removed successfully', 'status_code': 200}, status=200)
