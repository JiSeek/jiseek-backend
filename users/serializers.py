from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator


User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    is_korean = serializers.BooleanField()
    name = serializers.CharField(
        max_length=20,
        validators=[
            UniqueValidator(
                User.objects.all(),
                message="A user with this name already exists.",
            )
        ],
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["is_korean"] = self.validated_data.get("is_korean", "")
        data["name"] = self.validated_data.get("name", "")

        return data
