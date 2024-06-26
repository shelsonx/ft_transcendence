import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserInfo

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserInfo)
@receiver(post_delete, sender=UserInfo)
def update_positions(sender, instance, **kwargs):
    logger.info("update_positions signal triggered")
    users = UserInfo.objects.order_by('-scores')
    for index, user in enumerate(users, start=1):
        if user.position != index:
            user.position = index
            user.save(update_fields=['position'])
