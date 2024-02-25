from django.db import models
import uuid
from .login_type import LoginType
from django.contrib.auth.hashers import check_password, make_password

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    login_type = models.ForeignKey(LoginType, on_delete=models.CASCADE, null=False, blank=False)
    enable_2fa = models.BooleanField(default=False, null=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.user_name

    def check_password(self, password: str) -> bool:
        return check_password(password, self.password)