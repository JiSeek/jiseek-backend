from django.contrib.auth import get_user_model
from django.db import models

from core.utils import rename_imagefile_to_uuid
from config.storages import MediaStorage
from PIL import Image

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", null=True
    )
    image = models.ImageField(
        storage=MediaStorage(),
        upload_to=rename_imagefile_to_uuid,
        editable=True,
        blank=True,
        null=True,
    )
    board_favs = models.ManyToManyField(
        "boards.Board", related_name="board_favs", blank=True
    )
    food_favs = models.ManyToManyField(
        "foods.Food", related_name="food_favs", blank=True
    )

    def __str__(self):
        return f"{self.user.id}_profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # saving image first
        if self.image:
            img = Image.open(self.image)  # Open image using self

            if img.height > 300 or img.width > 300:
                new_img = (300, 300)
                img.thumbnail(new_img)
                img.save()  # saving image at the same path
