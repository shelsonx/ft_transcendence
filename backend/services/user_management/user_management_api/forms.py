from django import forms
from user_management_api.models.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'avatar', 'nickname', 'email']
        labels = {
            'name': 'Name',
            'avatar': 'Avatar',
            'nickname': 'Nickname',
            'two_factor_enabled': 'Two Factor Enabled',
            'email': 'Email',
            'chosen_language': 'Chosen Language',
            'status': 'Status'
        }
