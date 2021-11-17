from rest_framework.serializers import ModelSerializer
from .models import Board


class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "modified", "user")
