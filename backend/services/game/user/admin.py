from django.contrib import admin

# Local Folder
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ["username", "score", "rating", "winnings", "losses", "ties"]
