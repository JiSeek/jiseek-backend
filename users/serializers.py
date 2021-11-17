from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField()
    is_korean = serializers.BooleanField()

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["name"] = self.validated_data.get("name", "")
        data["is_korean"] = self.validated_data.get("is_korean", "")

        return data
