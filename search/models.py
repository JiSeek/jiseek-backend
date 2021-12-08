from django.db import models
from core.models import CoreModel
from core.utils import rename_imagefile_to_uuid
from config.storages import MediaStorage
from PIL import Image


class SearchImage(CoreModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="search_image"
    )
    photo = models.ImageField(
        null=True,
        storage=MediaStorage(),
        upload_to=rename_imagefile_to_uuid,
        editable=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.id}_searchphoto"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # saving image first
        if self.photo:
            img = Image.open(self.photo)  # Open image using self
            img = img.convert("RGB")
            img.load()
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(self.photo, "JPEG")  # saving image at the same path


class SearchResult(CoreModel):

    class_num = models.IntegerField(null=False)
    class_name = models.CharField(max_length=40)
    similarity = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    x_cord = models.IntegerField()
    y_cord = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="search", null=True
    )
    photo = models.ForeignKey(
        SearchImage, on_delete=models.CASCADE, related_name="search"
    )
    food = models.ForeignKey(
        "foods.Food",
        on_delete=models.CASCADE,
        related_name="search",
        null=True,
        default=1,
    )
