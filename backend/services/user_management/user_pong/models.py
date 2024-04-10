from django.db import models

# Create your models here.
class UserPong(models.Model):
    name = models.CharField(max_length=50, null=True)
    nickename = models.CharField(max_length=8, null=False)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
