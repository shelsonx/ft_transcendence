import uuid

from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import gettext_lazy as _

DEFAULT_AVATAR = "/media/avatars/default_avatar.jpeg"
USER_API = "https://localhost:8006"


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
    def average_points(self) -> int:
        total = self.total_games
        return self.score / total if total else 0

    @property
    def total_tournaments(self) -> int:
        return self.tournaments.all().count()

    @property
    def avatarUrl(self):
        if not self.avatar:
            self.avatar = DEFAULT_AVATAR
            self.save()
        return f"{USER_API}{self.avatar}"

    def reset(self):
        self.score = 0
        self.rating = 0
        self.winnings = 0
        self.losses = 0
        self.ties = 0
        self.save()

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
            "avatar": self.avatarUrl,
            "score": self.score,
            "rating": self.rating,
            "winnings": self.winnings,
            "losses": self.losses,
            "ties": self.ties,
        }

    def to_stats(self) -> dict:
        return {
            "id_msc": self.pk,
            "score": self.rating,
            "winnings": self.winnings,
            "losses": self.losses,
            "ties": self.ties,
        }
