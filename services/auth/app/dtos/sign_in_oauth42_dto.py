from django.db import models
from django import forms
from datetime import datetime, timedelta

class SignInOAuth42DtoForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    access_token = forms.CharField(max_length=100, required=True)
    expires_in = forms.IntegerField(required=True)

class SignInUpOAuth42Dto(models.Model):
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    access_token = models.CharField(max_length=100, null=False, blank=False)
    expires_in = models.IntegerField(null=False, blank=False)
    user_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return f"email: {self.email}, acess_token: {self.acess_token}, expires_in: {self.expires_in}"
    
    def _expire_in_datetime(self) -> datetime:
        return datetime.now() + timedelta(seconds=self.expires_in)
    
    def expire_to_hours(self) -> int:
        return self.expires_in // 3600
    
    def is_valid(self) -> bool:
        return datetime.now() < self._expire_in_datetime()
        
    class Meta:
            managed = False