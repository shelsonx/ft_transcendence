from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)


class User(models.Model):
    name = models.CharField(max_length=200)
