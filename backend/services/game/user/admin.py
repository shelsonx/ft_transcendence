from django.contrib import admin

# Local Folder
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    # readonly_fields = ()
    # list_filter = []

    # list_display = ["__str__"]
