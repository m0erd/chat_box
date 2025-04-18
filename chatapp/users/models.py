from django.contrib.auth.models import AbstractUser
from django.db import models
from chat.models import Channel
"""
chat ya da başka custom package importation bazen error verir, djangonun applicationları yükleme sırası her zaman
farklı için, istersek Lazy import denilen alternative uygulama ile bunu aşabiliriz. aşağıdaki snippetde örneklenmiştir.
runtime'da problem olmayacağı için böylede kalabilir. IDE kaynaklı da olabilir.
"""



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


"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    default_channel = models.ForeignKey(
        'chat.Channel',  # lazy reference! - app_name.ModelName
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_users"
    )

    def __str__(self):
        return self.username
"""
