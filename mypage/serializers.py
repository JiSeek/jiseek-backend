from django.contrib.auth import get_user_model
from rest_framework import serializers
from boards.models import Board
from foods.models import Food

User = get_user_model()


class BoardFavsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["pk", "content", "created"]


class FoodFavsSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source="image1")

    class Meta:
        model = Food
        fields = ["pk", "name", "image"]


class MyBoardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["pk", "created", "photo", "count"]
