from django.db import models
from django.contrib.auth.models import AbstractUser


class ButtonHistory(models.Model):
    fat = models.IntegerField(default=0)
    stupid = models.IntegerField(default=0)
    dumb = models.IntegerField(default=0)


class User(AbstractUser):
    username = models.CharField(max_length=128, unique=True)
    button_history = models.ForeignKey(ButtonHistory, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.username)
