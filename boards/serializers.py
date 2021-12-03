from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from .models import Board, Comment
from mypage.models import Profile


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "modified", "board", "user")


class BoardsSerializer(ModelSerializer):
    content = CharField(write_only=True)

    class Meta:
        model = Board
        fields = ("id", "photo", "content", "created", "user", "count")
        read_only_fields = (
            "id",
            "created",
            "modified",
            "user",
            "like_users",
            "count",
        )


class BoardSerializer(ModelSerializer):
    comment = CommentSerializer(read_only=True, many=True)
    is_fav = SerializerMethodField()

    def get_is_fav(self, obj):
        request = self.context.get("request")
        try:
            if request:
                user = request.user
                profile = Profile.objects.get(user_id=user.id)
                return obj in profile.board_favs.all()
        except Exception:
            return False
        return False

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
            "is_fav",
        )
