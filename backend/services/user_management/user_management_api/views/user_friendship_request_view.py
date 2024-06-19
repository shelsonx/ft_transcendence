from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from user_management_api.views.user_info import UserInfoView
from user_management_api.models.models import FriendshipRequest, Friendship
from user_management_api.exception.exception import MissingParameterException

from django.utils.translation import gettext as _

@method_decorator(csrf_exempt, name='dispatch')
class FriendshipRequestView(View):
    """
    Handles sending, accepting, and rejecting friend requests.
    """

    def get(self, request, user_id):
        friend_requests = FriendshipRequest.objects.filter(receiver_uuid=user_id, is_active=True)
        friend_requests_list = []
        for request in friend_requests:
            friend_requests_list.append({
                'id': request.id,
                'sender_id': request.sender.id,
                'sender_name': request.sender.name,
                'is_active': request.is_active,
            })
        return JsonResponse({'status': 'success', 'friend_requests': friend_requests_list, 'status_code': 200}, status=200)

    def post(self, request, user_id, friend_id=None):
        sent_friend_request_message = _('Friend request sent successfully')
        friend_request_already_sent_message = _('Friend request already sent')
        if friend_id is None:
            raise MissingParameterException("friend_id")
        sender = UserInfoView().get_user(user_id)
        receiver = UserInfoView().get_user(friend_id)
        if FriendshipRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).exists():
            return JsonResponse({'status': 'error', 'message': friend_request_already_sent_message, 'status_code': 400}, status=400)
        FriendshipRequest.objects.create(sender=sender, receiver=receiver, sender_uuid=sender.user_uuid, receiver_uuid=receiver.user_uuid)
        return JsonResponse({'status': 'success', 'message': sent_friend_request_message, 'status_code': 200}, status=200)

    def put(self, request, user_id, request_id=None):
        friend_request_accepted_message = _('Friend request accepted')
        friend_request_already_accepted_message = _('Friend request already accepted')
        if request_id is None:
            raise MissingParameterException("request_id")
        friend_request = FriendshipRequest.objects.get(id=request_id)
        friend_request.is_active = False
        try:
            Friendship.objects.create(user=friend_request.sender, friend=friend_request.receiver, user_uuid=friend_request.sender_uuid, friend_uuid=friend_request.receiver_uuid)
            Friendship.objects.create(user=friend_request.receiver, friend=friend_request.sender, user_uuid=friend_request.receiver_uuid, friend_uuid=friend_request.sender_uuid)
        except:
            return JsonResponse({'status': 'error', 'message': friend_request_already_accepted_message, 'status_code': 400}, status=400)
        friend_request.save()
        return JsonResponse({'status': 'success', 'message': friend_request_accepted_message, 'status_code': 200}, status=200)

    def delete(self, request, user_id, friend_id=None):
        friend_request_rejected_message = _('Friend request rejected')
        if friend_id is None:
            raise MissingParameterException("friend_id")
        FriendshipRequest.objects.filter(sender_id=friend_id, receiver_id=user_id, is_active=True).update(is_active=False)
        return JsonResponse({'status': 'success', 'message': friend_request_rejected_message, 'status_code': 200}, status=200)
