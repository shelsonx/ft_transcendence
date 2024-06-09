# from itertools import chain
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    # name = models.CharField(max_length=255)
    # avatarFileName = models.CharField(max_length=100, default="default_avatar.jpeg")
    # nickname = models.CharField(max_length=50)
    # score = models.IntegerField(default=0)

    @classmethod
    def validate_user_id(cls, *args, **kwargs) -> None:
        pass
        # user_id = kwargs.get("user_id")
        # request = args[1]
        # if request.current_user.sub != str(user_id):
        #     raise ForbiddenException()

    # @property
    # def avatarUrl(self):
    #     return f"https://"

    def to_json(self) -> dict:
        return {
            "id": self.pk,
            "username": self.username,
        }
