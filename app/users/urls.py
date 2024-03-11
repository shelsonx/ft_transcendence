from django.urls import path
from .views.views import UserInfoView, UserFriendshipView, UserBlockingView

urlpatterns = [
    path('user/', UserInfoView.as_view(), name='user_info'),
    path('user/<uuid:user_id>/', UserInfoView.as_view(), name='user_detail'),
    path('user/<uuid:user_id>/friends/', UserFriendshipView.as_view(), name='user_friends'),
    path('user/<uuid:user_id>/friends/<uuid:friend_id>/', UserFriendshipView.as_view(), name='modify_friends'),
    path('user/<uuid:user_id>/block/', UserBlockingView.as_view(), name='user_blocks'),
    path('user/<uuid:user_id>/block/<uuid:blocked_id>/', UserBlockingView.as_view(), name='modify_blocks'),
]
