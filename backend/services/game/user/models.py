import uuid

from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import gettext_lazy as _

DEFAULT_AVATAR = "/media/avatars/default_avatar.jpeg"


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    avatar = models.CharField(max_length=255, default=DEFAULT_AVATAR, blank=True)
    score = models.IntegerField(default=0)  # total points
    rating = models.IntegerField(default=0)
    winnings = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)

    @classmethod
    def get_object(cls, **fields):
        user = User.objects.filter(**fields)

        if user.count() > 1:
            raise MultipleObjectsReturned

        return user.first()

    @classmethod
    def anonymous(cls):
        return {
            "id": None,
            "username": _("anonymous"),
        }

    @property
    def total_games(self) -> int:
        return self.winnings + self.losses + self.ties

    @property
    def total_tournaments(self) -> int:
        return self.tournaments.all().count()

    @property
    def avatarUrl(self):
        if not self.avatar:
            self.avatar = DEFAULT_AVATAR
            self.save()
        return f"https://localhost:8006{self.avatar}"

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
