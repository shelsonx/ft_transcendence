# Django
from django import forms
from django.utils.translation import gettext_lazy as _

# First Party
from user.models import User


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "avatar"]


class UserSearchForm(UserForm):
    class Meta:
        model = User
        fields = ["username"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("insert nickname")}
            ),
        }
        labels = {
            "username": "",
        }
