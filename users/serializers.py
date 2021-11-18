from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator


User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField()
    is_korean = serializers.BooleanField()
    nickname = serializers.CharField(
        max_length=20,
        validators=[
            UniqueValidator(
                User.objects.all(),
                message="A user with this nickname already exists.",
            )
        ],
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["name"] = self.validated_data.get("name", "")
        data["is_korean"] = self.validated_data.get("is_korean", "")
        data["nickname"] = self.validated_data.get("nickname", "")

        return data
