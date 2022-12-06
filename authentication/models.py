from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    identifier = models.CharField(
        max_length=25, unique=True,
    )
    USERNAME_FIELD = "identifier"
