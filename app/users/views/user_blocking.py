from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..exception.exception import UserDoesNotExistException, InvalidUUIDException, InvalidFieldException
from ..models.models import User
from .user_info import UserInfoView

@method_decorator(csrf_exempt, name='dispatch')
class UserBlockingView(View):
    """
    Handles blocking and unblocking of users.

    - `get`: Retrieves the list of users blocked by the specified user.
    - `post`: Blocks a user for the specified user.
    - `delete`: Unblocks a previously blocked user for the specified user.
    """

    def get(self, request, user_id):
        try:
            user = UserInfoView().get_user(user_id)
            blocked_users = user.blocked_users.all()
            blocked_users_json = [blocked_user.as_json() for blocked_user in blocked_users]
            return JsonResponse({'status': 'success', 'blocked_users': blocked_users_json, 'status_code': 200}, status=200)
        except UserDoesNotExistException as e:
            return JsonResponse(e.to_dict(), status=e.status_code)

    def post(self, request, user_id, blocked_id):
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
        try:
            user = UserInfoView().get_user(user_id)
            blocked = UserInfoView().get_user(blocked_id)
            user.blocked_users.remove(blocked)
            return JsonResponse({'status': 'success', 'message': 'Blocked user removed successfully', 'status_code': 200}, status=200)
        except UserDoesNotExistException as e:
            return JsonResponse(e.to_dict(), status=e.status_code)
        except InvalidUUIDException as e:
            return JsonResponse(e.to_dict(), status=e.status_code)