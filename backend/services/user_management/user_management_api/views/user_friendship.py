from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user_management_api.views.user_info import UserInfoView

from user_management_api.exception.exception \
    import MissingParameterException

from django.utils.translation import gettext as _

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
        blocked_users = user.blocked_users.all()
        friends = user.friends.all()
        friends_json = [friend.as_json() for friend in friends]
        friends_json = [friend for friend in friends_json if friend not in blocked_users]
        return JsonResponse({'status': 'success', 'friends': friends_json, 'status_code': 200}, status=200)

    def delete(self, request, user_id, friend_id=None):
        print("user_id: ", user_id)
        friend_removed_message = _('Friend removed successfully')
        if friend_id is None:
            raise MissingParameterException("friend_id")
        user = UserInfoView().get_user(user_id)
        friend = UserInfoView().get_user(friend_id)
        user.friends.remove(friend)
        return JsonResponse({'status': 'success', 'message': friend_removed_message, 'status_code': 200}, status=200)
