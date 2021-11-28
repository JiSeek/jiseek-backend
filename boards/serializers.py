from rest_framework.serializers import ModelSerializer
from .models import Board, Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "modified", "board", "user")


class BoardSerializer(ModelSerializer):
    comment = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = (
            "id",
            "created",
            "modified",
            "user",
            "comment",
            "like_users",
            "count",
        )
