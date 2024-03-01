from django.db import models
from django import forms

class UserEditDtoForm(forms.Form):
    email = forms.EmailField(max_length=100)
    user_name = forms.CharField(max_length=100)
    enable_2fa = forms.BooleanField()
    password = forms.CharField()


class UserEditDto(models.Model):
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return f"email: {self.email}, password: {self.password}"