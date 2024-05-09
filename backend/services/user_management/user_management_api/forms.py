from django import forms
from user_management_api.models.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'nickname', 'email', 'chosen_language', 'two_factor_enabled', 'user_uuid']
        labels = {
            'user_uuid': 'User UUID',
            'name': 'Name',
            'avatar': 'Avatar',
            'nickname': 'Nickname',
            'two_factor_enabled': 'Two Factor Enabled',
            'email': 'Email',
            'chosen_language': 'Chosen Language',
            'status': 'Status'
        }
