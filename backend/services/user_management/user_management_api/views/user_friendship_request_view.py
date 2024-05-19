from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from user_management_api.views.user_info import UserInfoView
from user_management_api.models.models import FriendshipRequest, Friendship, User
from user_management_api.exception.exception import MissingParameterException

@method_decorator(csrf_exempt, name='dispatch')
class FriendshipRequestView(View):
    """
    Handles sending, accepting, and rejecting friend requests.
    """

    def get(self, request, user_id):
        friend_requests = FriendshipRequest.objects.filter(receiver_id=user_id)
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
        if friend_id is None:
            raise MissingParameterException("friend_id")
        sender = UserInfoView().get_user(user_id)
        receiver = UserInfoView().get_user(friend_id)
        if FriendshipRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).exists():
            return JsonResponse({'status': 'error', 'message': 'Friend request already sent', 'status_code': 400}, status=400)
        FriendshipRequest.objects.create(sender=sender, receiver=receiver)
        return JsonResponse({'status': 'success', 'message': 'Friend request sent successfully', 'status_code': 200}, status=200)

    def put(self, request, user_id, request_id=None):
        if request_id is None:
            raise MissingParameterException("request_id")
        friend_request = FriendshipRequest.objects.get(id=request_id)
        friend_request.is_active = False
        try:
            Friendship.objects.create(user=friend_request.sender, friend=friend_request.receiver)
            Friendship.objects.create(user=friend_request.receiver, friend=friend_request.sender)
        except:
            return JsonResponse({'status': 'error', 'message': 'Friend request already accepted', 'status_code': 400}, status=400)
        friend_request.save()
        return JsonResponse({'status': 'success', 'message': 'Friend request accepted', 'status_code': 200}, status=200)

    def delete(self, request, user_id, friend_id=None):
        if friend_id is None:
            raise MissingParameterException("friend_id")
        FriendshipRequest.objects.filter(sender_id=friend_id, receiver_id=user_id, is_active=True).update(is_active=False)
        return JsonResponse({'status': 'success', 'message': 'Friend request rejected', 'status_code': 200}, status=200)
