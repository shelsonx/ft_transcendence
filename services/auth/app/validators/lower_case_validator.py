from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class LowerCaseValidator:
    def __init__(self, lower_case_min=1):
        self.lower_case_min = lower_case_min

    def validate(self, password, user=None):
        upper_case_count = sum(1 for c in password if c.islower())
        if upper_case_count < self.lower_case_min:
            raise ValidationError(
                _(
                    "This password must contain at least %(lower_case_min)d character(s) in lowercase."
                ),
                code="password_too_short",
                params={"lower_case_min": self.lower_case_min},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(lower_case_min)d character(s) in lowercase."
            % {"lower_case_min": self.lower_case_min}
        )
