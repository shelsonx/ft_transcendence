from django.db import models
import uuid
from django.utils.translation import gettext as _

# Create your models here.
class UserInfo(models.Model):
    id_msc = models.UUIDField(default=uuid.uuid4, unique=True)
    full_name = models.CharField(_('full_name'), max_length=50, blank=False, null=False)
    nickname = models.CharField(_('nickname'), max_length=10, blank=False, null=False)
    scores = models.PositiveIntegerField(default=0)
    winnings = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)
    playing = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='static/images/%Y/%m/%d/',
                        blank=True, null=True, 
                        default='static/images/astronaut3.jpeg')