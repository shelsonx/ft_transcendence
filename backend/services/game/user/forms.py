from django import forms

from user.models import User

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        # fields = ["id"]
        exclude = []
