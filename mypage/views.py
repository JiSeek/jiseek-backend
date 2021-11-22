from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from .serializers import ProfileSerializer
from .models import Profile


class ProfileAPI(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [
        JWTCookieAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
