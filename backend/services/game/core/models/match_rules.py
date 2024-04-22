from datetime import timedelta
from typing import Collection

# Third Party
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class MatchRules(models.Model):

    class Meta:
        verbose_name_plural = _("Match Rules")
        db_table = "core_match_rules"
        constraints = [
            # models.CheckConstraint(check=models.Q(age__gte=18), name="age_gte_18"),
            models.CheckConstraint(
                check=Q(
                    ~Q(points_to_win__isnull=True)
                    | ~Q(match_total_points__isnull=True)
                    | ~Q(max_duration__isnull=True)
                ),
                name="all_rules_null",
                violation_error_message="At least one rule parameter must be setted",
            ),
        ]

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
    match_total_points = models.PositiveSmallIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name=_("Match total points"),
    )  # min=11

    max_duration = models.DurationField(
        default=timedelta(minutes=3),
        null=True,
        blank=True,
        verbose_name=_("Match maximum duration"),
    )

    def validate_constraints(self, exclude: Collection[str] | None = ...) -> None:
        if (
            self.points_to_win is None
            and self.match_total_points is None
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
