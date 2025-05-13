from django.db import models
from django.conf import settings


# class Channel(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     creator = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         related_name="channels",
#         on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return self.name
class Channel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='No description provided')
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="channels",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} in {self.channel.name}"


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} to {self.channel.name}: {self.content[:20]}"
