from django.db import models
import uuid

# Create your models here.
class UserInfo(models.Model):
    id_msc = models.UUIDField(default=uuid.uuid4, unique=True)
    full_name = models.CharField(max_length=50, blank=False, null=False)
    nickname = models.CharField(max_length=10, blank=False, null=False)
    scores = models.PositiveIntegerField(default=0)
    winnings = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)
    playing = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='media/avatars/',
                        blank=True, null=True, 
                        default='media/avatars/astronaut3.jpeg')