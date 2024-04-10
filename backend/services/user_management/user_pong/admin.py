from django.contrib import admin

from user_pong.models import UserPong

@admin.register(UserPong)
class UserPongAdmin(admin.ModelAdmin):
    pass

# Register your models here.
