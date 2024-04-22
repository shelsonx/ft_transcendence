from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_odd(value):
    if value is not None and value % 2 == 0:
        raise ValidationError(
            _("%(value)s is not an odd number"),
            params={"value": value},
        )
