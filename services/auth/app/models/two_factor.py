from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
import random
import uuid
from .user import User


class TwoFactor(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=now() + timedelta(hours=2))
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False)

    def is_valid(self, code):
        return self.expiration > now() and self.code == code
    
    def can_send_code(self, seconds: int):
        return self.created_at + timedelta(seconds=seconds) < now()
