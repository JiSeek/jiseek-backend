from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from rest_framework.validators import UniqueValidator


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=30)
    nickname = models.CharField(
        max_length=20,
        unique=True,
        error_messages={
            "unique": "A user with this phone number already exists.",
        },
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_korean = models.BooleanField(default=False)
    is_social_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
