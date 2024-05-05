from datetime import timedelta
from django import template

register = template.Library()

@register.filter()
def format_timedelta(td: timedelta):
    """Nice display for datetime.timedelta"""

    return f"{int(td.seconds / 60)} min {td.seconds % 60} s"
