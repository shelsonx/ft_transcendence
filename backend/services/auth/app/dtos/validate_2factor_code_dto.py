from django.db import models
from django import forms


class Validate2FactorCodeForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    two_factor_code = forms.CharField(max_length=6, required=False)


class Validate2FactorCodeDto(models.Model):
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    two_factor_code = models.CharField(max_length=6, null=True, blank=False)

    def __str__(self) -> str:
        return f"email: {self.email}"

    class Meta:
        managed = False
