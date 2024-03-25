from django.db import models
from django import forms

class SignInDtoForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)    
    password = forms.CharField(max_length=100, required=True)
    two_factor_code = forms.CharField(max_length=6, required=False)

class SignInDto(models.Model):
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    two_factor_code = forms.CharField(max_length=6, required=False)

    def __str__(self) -> str:
        return f"email: {self.email}, password: {self.password}"
    
    class Meta:
        managed = False