from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user_management_api.views.user_info import UserInfoView
from user_management_api.jwt.decorator import JWTAuthentication


from django.utils.translation import gettext as _

@method_decorator(csrf_exempt, name='dispatch')
class UserBlockingView(View):
    """
    Handles blocking and unblocking of users.

    - `get`: Retrieves the list of users blocked by the specified user.
    - `post`: Blocks a user for the specified user.
    - `delete`: Unblocks a previously blocked user for the specified user.
    """

    @JWTAuthentication()
    def get(self, request, user_id, blocked_id=None):
        if not blocked_id:
            user = UserInfoView().get_user(user_id)
            blocked_users = user.blocked_users.all()
            blocked_users_json = [blocked_user.as_json() for blocked_user in blocked_users]
            return JsonResponse({'status': 'success', 'blocked_users': blocked_users_json, 'status_code': 200}, status=200)
        else:
            user = UserInfoView().get_user(user_id)
            is_blocked = user.blocked_users.filter(user_uuid=blocked_id).exists()
            return JsonResponse({'status': 'success', 'is_blocked': is_blocked, 'status_code': 200}, status=200)

    @JWTAuthentication()
    def post(self, request, user_id, blocked_id):
        blocked_user_message = _('Blocked user added successfully')
        user = UserInfoView().get_user(user_id)
        blocked = UserInfoView().get_user(blocked_id)
        user.blocked_users.add(blocked)
        return JsonResponse({'status': 'success', 'message': blocked_user_message, 'status_code': 200}, status=200)

    @JWTAuthentication()
    def delete(self, request, user_id, blocked_id):
        blocked_user_removed_message = _('Blocked user removed successfully')
        user = UserInfoView().get_user(user_id)
        blocked = UserInfoView().get_user(blocked_id)
        user.blocked_users.remove(blocked)
        return JsonResponse({'status': 'success', 'message': blocked_user_removed_message, 'status_code': 200}, status=200)
