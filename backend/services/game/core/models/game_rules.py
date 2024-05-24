from datetime import timedelta
from typing import Collection

# Third Party
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# from core.validators.numbers import validate_odd


class GameRuleType(models.TextChoices):
    PLAYER_POINTS = "0", _("Player winner points")
    GAME_TOTAL_POINTS = "1", _("Game total points")
    GAME_DURATION = "2", _("Game duration")
    # MIXED_RULES = "3", _("Mixed rules")

    # __empty__ = _("(Unknown)")


class GameRules(models.Model):
    rule_type = models.CharField(
        max_length=1,
        choices=GameRuleType.choices,
        default=GameRuleType.PLAYER_POINTS,
        verbose_name=_("Game rule type"),
    )

    # original pong
    # for each player to reach eleven points before the opponent;
    # if self.score_a == 11 or self.score_b == 11 -> ended
    points_to_win = models.PositiveSmallIntegerField(
        default=11,
        null=True,
        blank=True,
        verbose_name=_("Points to win"),
    )  # min=5

    # different:
    # - sum of points == 11
    # if self.score_a + self.score_b == 11
    game_total_points = models.PositiveSmallIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name=_("Game total points"),
        # validators=[validate_odd],
    )  # min=11

    max_duration = models.DurationField(
        default=timedelta(minutes=3),
        null=True,
        blank=True,
        verbose_name=_("Game maximum duration"),
    )

    # paddle speed

    class Meta:
        verbose_name_plural = _("Game Rules")
        db_table = "core_game_rules"
        # unique_together = [
        #     ["rule_type", "points_to_win", "game_total_points", "max_duration"]
        # ]  # we don't wanna duplicated rules ---> usar UniqueConstraint
        constraints = [
            # models.CheckConstraint(check=models.Q(age__gte=18), name="age_gte_18"),
            models.CheckConstraint(
                check=Q(
                    ~Q(points_to_win__isnull=True)
                    | ~Q(game_total_points__isnull=True)
                    | ~Q(max_duration__isnull=True)
                ),
                name="all_rules_null",
                violation_error_message="At least one rule parameter must be setted",
            ),
            # models.CheckConstraint(
            #     check=Q(Q(points_to_win__gte=5) | Q(points_to_win__isnull=True)),
            #     name="points_to_win_validation",
            # ),
            # models.CheckConstraint(
            #     check=Q(
            #         Q(game_total_points__gte=7) | Q(game_total_points__isnull=True)
            #     ),
            #     name="game_total_points_validation",
            # ),
            # models.CheckConstraint(
            #     check=Q(
            #         Q(max_duration__gte=timedelta(minutes=3))
            #         | Q(max_duration__isnull=True)  # verificar se precisa do isnull..
            #         # e pode ser que ele tenha que ser antes...
            #     ),
            #     name="max_duration_validation",
            # ),
        ]

    def validate_constraints(self, exclude: Collection[str] | None = ...) -> None:
        if (
            self.points_to_win is None
            and self.game_total_points is None
            and self.max_duration is None
        ):
            pass
        return super().validate_constraints(exclude)

    # def full_clean(
    #     self,
    #     exclude: Collection[str] | None = ...,
    #     validate_unique: bool = ...,
    #     validate_constraints: bool = ...,
    # ) -> None:
    #     return super().full_clean(exclude, validate_unique, validate_constraints)

    def to_json(self) -> dict:
        return {
            "rule_type": self.rule_type,
            "points_to_win": self.points_to_win,
            "game_total_points": self.game_total_points,
            "max_duration": self.max_duration,
        }
