from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    pass


class User(AbstractBaseUser):

    status_choices = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    nickname = models.CharField(max_length=255, unique=True)
    two_factor_enabled = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    chosen_language = models.CharField(max_length=255, default='pt-br')
    status = models.CharField(max_length=255, choices=status_choices, default='inactive')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
            'nickname': self.nickname,
            'two_factor_enabled': self.two_factor_enabled,
            'email': self.email,
            'chosen_language': self.chosen_language,
            'status': self.status
        }

