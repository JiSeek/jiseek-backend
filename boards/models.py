from django.db import models
from core.models import CoreModel

from core.utils import rename_imagefile_to_uuid
from config.storages import MediaStorage
from PIL import Image


class Board(CoreModel):
    content = models.TextField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="boards"
    )
    photo = models.ImageField(
        null=True,
        storage=MediaStorage(),
        upload_to=rename_imagefile_to_uuid,
        editable=True,
        blank=True,
    )
    like_users = models.ManyToManyField("users.User", related_name="boards_count")
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.id}_board"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo)  # Open image using self

            if img.height > 800 or img.width > 800:
                new_img = (800, 800)
                img.thumbnail(new_img)
                img.save(self.photo)  # saving image at the same path

    class Meta:
        ordering = ["-created"]


class Comment(CoreModel):
    comment = models.CharField(max_length=255)
    board = models.ForeignKey(
        "Board", related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User", related_name="comments", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-modified"]
