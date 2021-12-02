from django.utils import timezone
from django.conf import settings
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import APISettings
from rest_framework_simplejwt.settings import USER_SETTINGS
from rest_framework_simplejwt.settings import DEFAULTS
from rest_framework_simplejwt.settings import IMPORT_STRINGS

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    is_korean = serializers.BooleanField()
    name = serializers.CharField(
        max_length=20,
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["is_korean"] = self.validated_data.get("is_korean", "")
        data["name"] = self.validated_data.get("name", "")

        return data


api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])

        data = {"access_token": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh_token"] = str(refresh)

        expires_at = (
            timezone.now()
            + getattr(settings, "SIMPLE_JWT", None)["ACCESS_TOKEN_LIFETIME"]
        )
        data["expires_at"] = int(round(expires_at.timestamp()))

        return data


class UserInfoRetrieveSerializer(ModelSerializer):
    image = serializers.ImageField(source="profile.image", read_only=True)

    class Meta:
        model = User
        fields = ["pk", "email", "name", "image"]


class UserInfoUpdateSerializer(ModelSerializer):
    email = serializers.EmailField(read_only=True)
    image = serializers.ImageField(source="profile.image")

    class Meta:
        model = User
        fields = ["pk", "email", "name", "image"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile")
        if profile_data:
            image = profile_data.get("image")
            if image:
                instance.profile.image = image
        name = validated_data.pop("name")
        instance.name = name

        instance.save()
        return instance
