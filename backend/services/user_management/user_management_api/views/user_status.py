from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user_management_api.views.user_info import UserInfoView
from user_management_api.jwt.decorator import JWTAuthentication
import json


from django.utils.translation import gettext as _

@method_decorator(csrf_exempt, name='dispatch')
class UserStatusView(View):
    """
    Handles user status operations.
    `get`: Retrieves the status of the specified user.
    `post`: Updates the status of the specified user.
    """

    @JWTAuthentication()
    def get(self, request, user_id):
        user = UserInfoView().get_user(user_id)
        return JsonResponse({'status': 'success', 'status_code': 200, 'user_status': user.status}, status=200)

    def post(self, request, user_id):
        user_status_updated_message = _('User status updated successfully')
        user = UserInfoView().get_user(user_id)
        # get status from payload
        user.status = json.loads(request.body.decode('utf-8'))['status']
        user.save()
        return JsonResponse({'status': 'success', 'message': user_status_updated_message, 'status_code': 200}, status=200)