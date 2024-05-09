from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from user_management_api.views.user_blocking import UserBlockingView
from user_management_api.views.user_info import UserInfoView
from user_management_api.views.user_friendship import UserFriendshipView
from user_management_api.views.user_friendship_request_view import FriendshipRequestView

urlpatterns = [
    path('user/', UserInfoView.as_view(), name='user_info'),
    path('user/<uuid:user_id>/', UserInfoView.as_view(), name='user_detail'),
    path('user/<uuid:user_id>/friends/', UserFriendshipView.as_view(), name='user_friends'),
    path('user/<uuid:user_id>/friends/<uuid:friend_id>/', UserFriendshipView.as_view(), name='modify_friends'),
    path('user/<uuid:user_id>/block/', UserBlockingView.as_view(), name='user_blocks'),
    path('user/<uuid:user_id>/block/<uuid:blocked_id>/', UserBlockingView.as_view(), name='modify_blocks'),
    path('user/<uuid:user_id>/friend_request/', FriendshipRequestView.as_view(), name='friend_request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)