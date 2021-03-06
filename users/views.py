import json
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.exceptions import MethodNotAllowed
from datetime import timedelta
from .serializers import (
    CustomTokenRefreshSerializer,
    UserInfoRetrieveSerializer,
    UserInfoUpdateSerializer,
    UserInfoPartialUpdateSerializer,
)
from dj_rest_auth.registration.serializers import VerifyEmailSerializer
from dj_rest_auth.utils import jwt_encode


User = get_user_model()
S3_BASE_URL = settings.S3_BASE_URL


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh), str(refresh.access_token)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(LoginView):
    def get_response(self):
        orginal_response = super().get_response()
        expires_at = timezone.now() + timedelta(hours=2)
        expires_at_data = {
            "expires_at": int(round(expires_at.timestamp())),
        }
        orginal_response.data.update(expires_at_data)
        orginal_response.data["user"]["name"] = self.user.name
        if self.user.profile.image:
            orginal_response.data["user"]["image"] = S3_BASE_URL + str(
                self.user.profile.image
            )
        else:
            orginal_response.data["user"]["image"] = None
        orginal_response.data["social_platform"] = self.user.social_platform

        return orginal_response


class GoogleLoginView(View):
    def post(self, request):  # id_token??? key ????????? ??????
        data = json.loads(request.body)
        access_token = data.get("key", None)
        url = "https://oauth2.googleapis.com/tokeninfo?id_token="  # ????????? ???????????? ????????? ????????? ???????????? ?????? google api??????
        response = requests.get(url + access_token)  # ????????? id_token??? ?????? ????????? ??????
        user = response.json()  # ????????? ????????? json????????? ????????? ??????

        if User.objects.filter(email=user["email"]).exists():
            return JsonResponse({"detail": "The email already exits"}, status=400)

        elif User.objects.filter(
            social_login_id=user["sub"], social_platform="kakao"
        ).exists():  # ????????? ?????????????????? ??????
            user = User.objects.get(social_login_id=user["sub"])  # ????????? ???????????? ????????? ??????
            user.last_login = timezone.now()
            user.save()
            refresh_token, access_token = get_tokens_for_user(user)
            expires_at = (
                timezone.now()
                + getattr(settings, "SIMPLE_JWT", None)["ACCESS_TOKEN_LIFETIME"]
            )
            if user.profile.image:
                image = S3_BASE_URL + str(user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt??????, ??????, ?????? ?????????????????? ??????
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "name": user.name,
                        "pk": user.id,
                        "image": image,
                        "social_platform": user.social_platform,
                    },
                    "expires_at": int(round(expires_at.timestamp())),
                },
                status=200,
            )
        else:
            user = User(  # ???????????? ?????????????????? ?????? ?????? ?????? ????????? ??????(email??? ?????? ?????? ?????? ??????, ????????? ????????????, ????????? None?????? ??????)
                social_login_id=user["sub"],
                name=user["name"],
                social_platform="google",
                email=user.get("email", None),
                last_login=timezone.now(),
            )
            user.save()  # DB??? ??????
            refresh_token, access_token = get_tokens_for_user(user)
            if user.profile.image:
                image = S3_BASE_URL + str(user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt??????, ??????, ?????? ?????????????????? ??????
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "name": user.name,
                        "pk": user.id,
                        "image": image,
                        "social_platform": user.social_platform,
                    },
                    "expires_at": timezone.now()
                    + getattr(settings, "SIMPLE_JWT", None)["ACCESS_TOKEN_LIFETIME"],
                },
                status=200,
            )


class KakaoLoginView(View):  # ????????? ?????????
    def post(self, request):  # ?????????????????? ???????????? access_token?????? ????????? ?????? ????????????
        data = json.loads(request.body)
        access_token = data.get("key", None)
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://kapi.kakao.com/v2/user/me"  # Authorization(??????????????? ?????? ??????)??? ???????????? ????????? ????????? ???????????? ?????? ????????? API ??????
        response = requests.request(
            "GET", url, headers=headers
        )  # API??? ???????????? ????????? ????????? response??? ??????
        user = response.json()

        if User.objects.filter(
            social_login_id=user["id"], social_platform="kakao"
        ).exists():  # ????????? ?????????????????? ???????????? ??????
            user = User.objects.get(social_login_id=user["id"])
            user.last_login = timezone.now()
            user.save()
            refresh_token, access_token = get_tokens_for_user(user)
            expires_at = (
                timezone.now()
                + getattr(settings, "SIMPLE_JWT", None)["ACCESS_TOKEN_LIFETIME"]
            )
            if user.profile.image:
                image = S3_BASE_URL + str(user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt??????, ??????, ?????? ?????????????????? ??????
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "name": user.name,
                        "pk": user.id,
                        "image": image,
                        "social_platform": user.social_platform,
                    },
                    "expires_at": int(round(expires_at.timestamp())),
                },
                status=200,
            )
        else:
            user = User(
                social_login_id=user["id"],
                name=user["properties"]["nickname"],  # kakao??? ???????????? ?????????
                social_platform="kakao",
                email=user["properties"].get("email", None),
                last_login=timezone.now(),
            )
            user.save()

            refresh_token, access_token = get_tokens_for_user(user)
            if user.profile.image:
                image = S3_BASE_URL + str(user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt??????, ??????, ?????? ?????????????????? ??????
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "name": user.name,
                        "pk": user.id,
                        "image": image,
                        "social_platform": user.social_platform,
                    },
                    "expires_at": timezone.now()
                    + getattr(settings, "SIMPLE_JWT", None)["ACCESS_TOKEN_LIFETIME"],
                },
                status=200,
            )


class NaverLoginView(View):  # ????????? ?????????
    def post(self, request):
        data = json.loads(request.body)
        access_token = data.get("key", None)
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://openapi.naver.com/v1/nid/me"  # Authorization(??????????????? ?????? ??????)??? ???????????? ????????? ????????? ???????????? ?????? ????????? API ??????
        response = requests.request(
            "GET", url, headers=headers
        )  # API??? ???????????? ????????? ????????? response??? ??????
        user = response.json()

        if User.objects.filter(email=user["response"]["email"]).exists():
            return JsonResponse({"detail": "The email already exits"}, status=400)

        elif User.objects.filter(
            social_login_id=user["response"]["id"], social_platform="naver"
        ).exists():  # ????????? ?????????????????? ???????????? ??????
            user = User.objects.get(social_login_id=user["response"]["id"])
            user.last_login = timezone.now()
            user.save()
            refresh_token, access_token = get_tokens_for_user(user)
            if user.profile.image:
                image = S3_BASE_URL + str(user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt??????, ??????, ?????? ?????????????????? ??????
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "name": user.name,
                        "pk": user.id,
                        "image": image,
                        "social_platform": user.social_platform,
                    },
                    "expires_at": timezone.now()
                    + getattr(settings, "SIMPLE_JWT", None)["ACCESS_TOKEN_LIFETIME"],
                },
                status=200,
            )
        else:
            user = User(
                social_login_id=user["response"]["id"],
                name=user["response"]["nickname"],
                social_platform="naver",
                email=user["response"]["email"],
                last_login=timezone.now(),
            )
            user.save()
            refresh_token, access_token = get_tokens_for_user(user)
            if user.profile.image:
                image = S3_BASE_URL + str(user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt??????, ??????, ?????? ?????????????????? ??????
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "name": user.name,
                        "pk": user.id,
                        "image": image,
                        "social_platform": user.social_platform,
                    },
                    "expires_at": timezone.now()
                    + getattr(settings, "SIMPLE_JWT", None)["ACCESS_TOKEN_LIFETIME"],
                },
                status=200,
            )


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class UserInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = UserInfoRetrieveSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == "PUT":
            serializer_class = UserInfoUpdateSerializer
        elif self.request.method == "PATCH":
            serializer_class = UserInfoPartialUpdateSerializer
        return serializer_class


class CustomVerifyEmailView(VerifyEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ("POST", "OPTIONS", "HEAD")

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]
        confirmation = self.get_object()
        confirmation.confirm(self.request)

        self.user = confirmation.email_address.user
        self.user.last_login = timezone.now()
        access_token, refresh_token = jwt_encode(self.user)
        if self.user.profile.image:
            image = S3_BASE_URL + str(self.user.profile.image)
        else:
            image = None
        return JsonResponse(
            {  # jwt??????, ??????, ?????? ?????????????????? ??????
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
                "user": {
                    "email": self.user.email,
                    "name": self.user.name,
                    "image": image,
                    "pk": self.user.id,
                },
                "expires_at": timezone.now()
                + getattr(settings, "SIMPLE_JWT", None)["ACCESS_TOKEN_LIFETIME"],
            },
            status=200,
        )
