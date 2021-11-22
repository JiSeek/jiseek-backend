from django.contrib.auth import get_user_model
from rest_framework import serializers
from boards.serializers import BoardSerializer
from foods.serializers import FoodSerializer
from .models import Profile

User = get_user_model()


class BoardFavsSerializer(serializers.ModelSerializer):
    boards = BoardSerializer(source="board_favs", read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ["boards"]


class FoodFavsSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(source="food_favs", read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ["foods"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["image"]


class UpdateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["name", "profile"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        if profile_data is not None:
            instance.profile.image = profile_data["image"]
            instance.profile.save()
        return super().update(instance, validated_data)
