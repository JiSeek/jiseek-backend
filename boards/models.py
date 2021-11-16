from django.db import models
from core.models import CoreModel


class Board(CoreModel):
    content = models.TextField()
    # user = models.ForeignKey(
    #     "users.User", on_delete=models.CASCADE, related_name="boards"
    # )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-modified"]


class Photo(CoreModel):
    caption = models.CharField(max_length=100)
    file = models.ImageField()
    board = models.OneToOneField(
        "boards.Board", verbose_name="board_photo", on_delete=models.CASCADE
    )
