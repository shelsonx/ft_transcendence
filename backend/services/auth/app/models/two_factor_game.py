from django.db import models
from django.utils.timezone import now
from datetime import timedelta
import uuid
from .user import User

def default_expiration():
    return now() + timedelta(hours=2)

class TwoFactorGame(models.Model):

    class GameType(models.TextChoices):
        INDIVIDUAL_GAME = 'INDIVIDUAL_GAME', 'Individual Game'
        TOURNAMENT = 'TOURNAMENT', 'Tournament'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=default_expiration)
    user_receiver_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_games')
    user_requester_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='requested_games')
    game_type = models.CharField(max_length=50, choices=GameType.choices, default=GameType.INDIVIDUAL_GAME)
    game_id = models.BigIntegerField(null=False, blank=False)

    def is_valid(self, code):
        return self.expiration > now() and self.code == code

    def can_send_code(self, seconds: int):
        return self.created_at + timedelta(seconds=seconds) < now()
