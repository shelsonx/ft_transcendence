from django.db import models
from django import forms
from ..models.two_factor_game import TwoFactorGame
from django.contrib.postgres.fields import ArrayField
import uuid
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

MAX_UUIDS = 100
class UUIDArrayField(forms.Field):
    """ Custom field representing an array of up to MAX_UUIDS uuid4 strings """
    def clean(self, value):
        if type(value) != type([]):
            raise ValidationError(self.error_messages['not_a_list'])
        if len(value) > MAX_UUIDS:
            raise ValidationError(self.error_messages['too_many_values'])
        try:
            for v in value:
                uuid.UUID(v, version=4) # ValueError if not a valid uuid4
            return [uuid.UUID(uui_str) for uui_str in value]
        except:
            raise ValidationError(self.error_messages['invalid_uuid'])

class CodeUUIDArrayField(forms.Field):
    def is_valid_uuid(self, uuid_str):
        try:
            uuid.UUID(uuid_str)
            return True
        except ValueError:
            return False

    def is_valid_data(self, data):
        if not isinstance(data, list) or len(data) > MAX_UUIDS:
            return False
        for item in data:
            if not isinstance(item, dict) or len(item) != 1:
                return False
            key, value = next(iter(item.items()))
            if not isinstance(key, str) or len(key) != 6 or not key.isdigit() or not self.is_valid_uuid(value):
                return False
        return True

    def clean(self, value):
        if not isinstance(value, list):
            raise ValidationError(self.error_messages['not_a_list'])
        if not self.is_valid_data(value):
            raise ValidationError(self.error_messages['invalid_uuid'])
        return value

class SendGame2FactorCodeForm(forms.Form):
    user_receiver_ids = UUIDArrayField(required=True,
                                      error_messages={
                                          'not_a_list': _('The user_receiver_id field must be an array of uuids.'),
                                          'too_many_values': _('The user_receiver_id field must contain at most %(max_uuids)d uuids.') % {'max_uuids': MAX_UUIDS},
                                          'invalid_uuid': _('The user_receiver_id field must contain only valid uuids.')})
    user_requester_id = forms.UUIDField(required=True)
    game_type = forms.CharField(max_length=50, required=True)
    game_id = forms.IntegerField(required=True)


class SendGame2FactorCodeDto(models.Model):
    user_receiver_ids = ArrayField(models.UUIDField(blank=False, null=False), default=list)
    user_requester_id = models.UUIDField(blank=False, null=False)
    game_type = models.CharField(max_length=50, choices=TwoFactorGame.GameType.choices, default=TwoFactorGame.GameType.INDIVIDUAL_GAME)
    game_id = models.BigIntegerField(null=False, blank=False)


    def __str__(self) -> str:
        return f"user_receiver_ids: {self.user_receiver_ids}, user_requester_id: {self.user_requester_id}, game_type: {self.game_type}, game_id: {self.game_id}"

    class Meta:
        managed = False

class ValidateGame2FactorCodeForm(forms.Form):
    user_requester_id = forms.UUIDField(required=True)
    code_user_receiver_id = CodeUUIDArrayField(required=True,
                                      error_messages={
                                          'not_correct_format': _('The code_user_receiver_id field must be an array of code and uuids.'),
                                          'too_many_values': _('The code_user_receiver_id field must contain at most %(max_uuids)d uuids.') % {'max_uuids': MAX_UUIDS},
                                          'invalid_uuid': _('The code_user_receiver_id field must contain only valid uuids.')})
    game_id = forms.IntegerField(required=True)
    game_type = forms.CharField(max_length=50, required=True)

class ValidateGame2FactorCodeDto(models.Model):
    user_requester_id = models.UUIDField(blank=False, null=False)
    code_user_receiver_id = models.JSONField(null=True, blank=True)
    game_id = models.BigIntegerField(null=False, blank=False)
    game_type = models.CharField(max_length=50, choices=TwoFactorGame.GameType.choices, default=TwoFactorGame.GameType.INDIVIDUAL_GAME)

    def __str__(self) -> str:
        return f"user_requester_id: {self.user_requester_id}, code_user_receiver_id: {self.code_user_receiver_id}, game_id: {self.game_id}, game_type: {self.game_type}"

    class Meta:
        managed = False
