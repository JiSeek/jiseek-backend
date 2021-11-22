from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, **kwargs):
        if not "email" in kwargs:
            raise ValueError("Users must have an email address")
        if not "password" in kwargs:
            raise ValueError("Users must have an password")

        user = self.model(
            email=self.normalize_email(kwargs.get("email")),
        )
        user.set_password(self.normalize_email(kwargs.get("password")))
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        new_superuser = self.create_user(**kwargs)
        new_superuser.is_admin = True
        new_superuser.is_superuser = True
        new_superuser.is_staff = True
        new_superuser.save(using=self._db)
        return new_superuser
