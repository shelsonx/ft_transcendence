from django.contrib import admin

# Local Folder
from .models import User


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     model = User
#     readonly_fields = ("created_by", "company")
#     list_filter = ["stepper_type"]

#     list_display = ["__str__", "created_by", "company", "datetime", "stepper_type"]
