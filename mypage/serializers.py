from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # nickname = serializers.CharField(source="profile.nickname")

    class Meta:
        model = Profile
        fields = [
            "nickname",
        ]
