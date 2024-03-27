from django.db import models
from django import forms
from ..interfaces.dtos.base_sign_up_dto import BaseSignUpDto

class SignUpDtoForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)    
    password = forms.CharField(max_length=100, required=True)
    user_name = forms.CharField(max_length=100, required=True)
    two_factor_code = forms.CharField(max_length=6, required=False)

class SignUpDto(BaseSignUpDto):
    password = models.CharField(max_length=100, null=False, blank=False)
    two_factor_code = models.CharField(max_length=6, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"email: {self.email}, password: {self.password}, user_name: {self.user_name}"
    
    class Meta:
        managed = False