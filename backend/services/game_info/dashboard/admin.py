from django.contrib import admin
from .models import UserInfo
# Register your models here.

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nickname', 'scores', 'winnings', 'losses', 'position', 'status', 'playing', 'photo')
    list_filter = ('full_name', 'nickname', 'scores', 'winnings', 'losses', 'position', 'status', 'playing', 'photo')
    search_fields = ('full_name', 'nickname', 'scores', 'winnings', 'losses', 'position', 'status', 'playing', 'photo')