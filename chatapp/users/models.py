from django.contrib.auth.models import AbstractUser
from django.db import models
from chat.models import Channel


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    default_channel = models.ForeignKey(
        Channel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_users"
    )

    def __str__(self):
        return self.username
