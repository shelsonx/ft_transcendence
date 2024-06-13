# from itertools import chain
import uuid

from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from django.http import Http404
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    # name = models.CharField(max_length=255)
    # avatarFileName = models.CharField(max_length=100, default="default_avatar.jpeg")
    # nickname = models.CharField(max_length=50)
    # score = models.IntegerField(default=0)

    @classmethod
    def get_object(cls, **fields):
        user = User.objects.filter(**fields)

        if user.count() > 1:
            raise MultipleObjectsReturned

        user = user.first()
        if not user:
            # TODO: SHEELA - call auth api and user management api to get data and
            # create user
            pass

        return user

    @classmethod
    def anonymous(cls):
        return {
            "id": None,
            "username": _("anonymous"),
        }

    # @property
    # def avatarUrl(self):
    #     return f"https://"

    def __str__(self):
        return self.username

    def resume_to_json(self) -> dict:
        return {
            "id": self.pk,
            "username": self.username,
        }

    def to_json(self) -> dict:
        return {
            "id": self.pk,
            "username": self.username,
        }
