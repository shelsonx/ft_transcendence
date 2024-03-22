from django.db import models

class BaseSignUpDto(models.Model):
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    user_name = models.CharField(max_length=100, null=False, blank=False)
    
    class Meta:
        managed = False