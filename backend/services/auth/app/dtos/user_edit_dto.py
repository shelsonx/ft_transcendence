from django.db import models
from django import forms


class UserEditDtoForm(forms.Form):
    user_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length=100, required=False)
    enable_2fa = forms.BooleanField(required=False)
    password = forms.CharField(required=False)
    old_password = forms.CharField(required=False)


class UserEditDto(models.Model):
    user_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    enable_2fa = models.BooleanField()
    password = models.CharField(max_length=100, blank=False)
    old_password = models.CharField(max_length=100, blank=False)

    def __str__(self) -> str:
        return f"UserEditDto: user_name={self.user_name}, email={self.email}, enable_2fa={self.enable_2fa}, password={self.password}, old_password={self.old_password}"

    class Meta:
        managed = False
