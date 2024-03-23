from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
import random
import uuid
from .user import User

class TwoFactorEmailModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=now() + timedelta(hours=2)) 
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False)
 
    def save(self):
        self.code = self.generate_code()
        return super().save()

    def generate_code(self):
        return str(random.randint(100000, 999999))
    
    def send_two_factor_email(self, subject, body):
        send_mail(subject, body, [self.user.email])

    def can_be_sent(self, code):
        return self.expiration < now() and self.code == code

    def is_expired(self):
        return self.expiration < now()
