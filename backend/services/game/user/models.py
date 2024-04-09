from django.db import models

# Create your models here.

class User(models.Model):
	id_reference = models.IntegerField(min=0)

