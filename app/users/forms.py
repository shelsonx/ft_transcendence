from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'avatar', 'nickname', 'two_factor_enabled', 'email']
        labels = {
            'name': 'Name',
            'avatar': 'Avatar',
            'nickname': 'Nickname',
            'two_factor_enabled': 'Two Factor Enabled',
            'email': 'Email'
        }