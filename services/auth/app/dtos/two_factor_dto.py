from django.db import models
from django import forms
from ..interfaces.dtos.base_sign_up_dto import BaseSignUpDto

class TwoFactorDto(models.Model):
    user_id = models.UUIDField(null=False, blank=False)
    code = models.CharField(max_length=6, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    
    def __str__(self) -> str:
        return f"user_id: {self.user_id}, code: {self.code}"
    
    class Meta:
        managed = False