from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from .managers import CustomUserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, unique=True)
    # avatar = models.ImageField(upload_to=upload_image, editable=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_korean = models.BooleanField(default=False)
    is_social_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
