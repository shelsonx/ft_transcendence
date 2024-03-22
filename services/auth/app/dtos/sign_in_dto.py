from django.db import models
from django import forms

class SignInDtoForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)    
    password = forms.CharField(max_length=100, required=True)

class SignInDto(models.Model):
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return f"email: {self.email}, password: {self.password}"
    
    class Meta:
        managed = False