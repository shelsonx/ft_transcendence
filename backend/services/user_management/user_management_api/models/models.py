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
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name='added_friends')
    blocked_users = models.ManyToManyField('self', symmetrical=False, related_name='blocked_by')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def as_json(self):
        friends = self.friends.all()
        friends_json = [friend.as_json() for friend in friends]
        blocked_users = self.blocked_users.all()
        blocked_users_json = [blocked_user.as_json() for blocked_user in blocked_users]
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
            'nickname': self.nickname,
            'two_factor_enabled': self.two_factor_enabled,
            'email': self.email,
            'chosen_language': self.chosen_language,
            'status': self.status,
            'friends': friends_json,
            'blocked_users': blocked_users_json
        }


class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_creator')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_receiver')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'friend']

    def __str__(self):
        return f'{self.user} is friends with {self.friend}'

class BlockedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking_user')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'blocked_user']

    def __str__(self):
        return f'{self.user} has blocked {self.blocked_user}'
