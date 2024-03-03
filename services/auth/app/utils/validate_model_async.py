from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from ..exceptions.validation_error_exception import ValidationErrorException
from django.db import models
from .call_async import call_async

async def validate_model_async(model: models.Model):
  try:
        await call_async(model.full_clean)
  except ValidationError as e:
        raise ValidationErrorException(e.message_dict)