from django.db import models
import uuid

class LoginType(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100, unique=True, null=False, blank=False)

  def __str__(self) -> str:
    return self.name