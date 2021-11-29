from django.contrib.auth import get_user_model
from django.db import models

from core.utils import image_resize
from config.storages import MediaStorage

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", null=True
    )
    image = models.ImageField(
        storage=MediaStorage(), editable=True, blank=True, null=True
    )
    board_favs = models.ManyToManyField(
        "boards.Board", related_name="board_favs", blank=True
    )
    food_favs = models.ManyToManyField(
        "foods.Food", related_name="food_favs", blank=True
    )

    def __str__(self):
        return f"{self.user.name} profile"

    def save(self, *args, **kwargs):
        if self.image:
            image_resize(self.image, 512, 512)
        super().save(*args, **kwargs)
