from django.contrib import admin
from .models import Board, Comment


@admin.register(Board)
class CustomBoardAdmin(admin.ModelAdmin):

    """Custom Board Admin"""

    list_display = ("id", "user", "content")
    list_filter = ("user",)


@admin.register(Comment)
class CustomCommentAdmin(admin.ModelAdmin):

    """Custom Comment Admin"""

    list_display = ("id", "user", "content")
    list_filter = ("user",)
