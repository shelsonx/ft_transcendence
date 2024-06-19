from django import forms
from user_management_api.models.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'nickname', 'chosen_language', 'two_factor_enabled', 'user_uuid', 'avatar', 'email']