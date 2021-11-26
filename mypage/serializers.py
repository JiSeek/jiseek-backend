from django.contrib.auth import get_user_model
from rest_framework import serializers
from boards.serializers import BoardSerializer
from foods.serializers import FoodSerializer
from .models import Profile
from boards.models import Board
from foods.models import Food

User = get_user_model()


class BoardFavsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["pk", "content", "created"]


class FoodFavsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["pk", "name"]


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
