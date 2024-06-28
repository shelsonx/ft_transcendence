from django.db import models
import uuid

DEFAULT_AVATAR = "/media/avatars/default_avatar.jpeg"
USER_API = "https://localhost:8006"

# Create your models here.
class UserInfo(models.Model):
    id_msc = models.UUIDField(default=uuid.uuid4, unique=True)
    full_name = models.CharField(max_length=50, blank=False, null=False)
    nickname = models.CharField(max_length=50, blank=False, null=False, unique=True)
    scores = models.PositiveIntegerField(default=0)
    winnings = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)
    playing = models.BooleanField(default=False)
    photo = models.CharField(max_length=255, default=DEFAULT_AVATAR, blank=True)
    
    @property
    def avatarUrl(self):
        if not self.avatar:
            self.avatar = DEFAULT_AVATAR
            self.save()
        return f"{USER_API}{self.avatar}"
    
    class Meta:
        ordering = ['-scores']
