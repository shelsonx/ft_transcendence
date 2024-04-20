from django.db import models

# Create your models here.
class UserInfo(models.Model):
    full_name = models.CharField(max_length=50, blank=False, null=False)
    nickname = models.CharField(max_length=10, blank=False, null=False)
    scores = models.IntegerField(default=0)
    winnings = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    position = models.IntegerField()
    status = models.BooleanField(default=False)
    playing = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='static/images/%Y/%m/%d/',
                        blank=True, null=True, 
                        default='static/images/avatar_user_icon2.png')