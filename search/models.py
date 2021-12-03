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
        if self.photo:
            img = Image.open(self.photo)
            if img.height > 800 or img.width > 800:
                new_img = (800, 800)
                img.thumbnail(new_img)
                img.save(self.photo)

        super().save(*args, **kwargs)


class SearchResult(CoreModel):

    class_num = models.IntegerField(null=False)
    class_name = models.CharField(max_length=40)
    similarity = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    x_cord = models.IntegerField()
    y_cord = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="search"
    )
    photo = models.ForeignKey(
        SearchImage, on_delete=models.CASCADE, related_name="search"
    )
