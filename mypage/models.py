from django.contrib.auth import get_user_model
from django.db import models

from PIL import Image
from .utils import upload_image


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(
        upload_to=upload_image, editable=True, blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.username} profile"

    # # Override the save method of the model
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)  # Open image

    #     # resize image
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)  # Resize image
    #         img.save(self.image.path)  # Save it again and override the larger image
