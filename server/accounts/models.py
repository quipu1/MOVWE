from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from server.validators import AlphanumericUsernameValidator

# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("해당 아이디의 사용자가 존재합니다."),
        },
    )
