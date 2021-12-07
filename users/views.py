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
import requests, json
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
    def post(self, request):  # id_token만 key 값으로 받기
        data = json.loads(request.body)
        access_token = data.get("key", None)
        url = "https://oauth2.googleapis.com/tokeninfo?id_token="  # 토큰을 이용해서 회원의 정보를 확인하기 위한 google api주소
        response = requests.get(url + access_token)  # 구글에 id_token을 보내 디코딩 요청
        user = response.json()  # 유저의 정보를 json화해서 변수에 저장

        if User.objects.filter(email=user["email"]).exists():
            return JsonResponse({"detail": "The email already exits"}, status=400)

        elif User.objects.filter(
            social_login_id=user["sub"], social_platform="kakao"
        ).exists():  # 기존에 가입했었는지 확인
            user = User.objects.get(social_login_id=user["sub"])  # 가입된 데이터를 변수에 저장
            user.last_login = timezone.now()
            user.save()
            refresh_token, access_token = get_tokens_for_user(user)
            expires_at = (
                timezone.now()
                + getattr(settings, "SIMPLE_JWT", None)["ACCESS_TOKEN_LIFETIME"]
            )
            if self.user.profile.image:
                image = S3_BASE_URL + str(self.user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt토큰, 이름, 타입 프론트엔드에 전달
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
            user = User(  # 처음으로 소셜로그인을 했을 경우 회원 정보를 저장(email이 없을 수도 있다 하여, 있으면 저장하고, 없으면 None으로 표기)
                social_login_id=user["sub"],
                name=user["name"],
                social_platform="google",
                email=user.get("email", None),
                last_login=timezone.now(),
            )
            user.save()  # DB에 저장
            refresh_token, access_token = get_tokens_for_user(user)
            if self.user.profile.image:
                image = S3_BASE_URL + str(self.user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt토큰, 이름, 타입 프론트엔드에 전달
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


class KakaoLoginView(View):  # 카카오 로그인
    def post(self, request):  # 프론트로부터 전달받은 access_token으로 사용자 정보 가져오기
        data = json.loads(request.body)
        access_token = data.get("key", None)
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://kapi.kakao.com/v2/user/me"  # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 카카오 API 주소
        response = requests.request(
            "GET", url, headers=headers
        )  # API를 요청하여 회원의 정보를 response에 저장
        user = response.json()

        if User.objects.filter(
            social_login_id=user["id"], social_platform="kakao"
        ).exists():  # 기존에 소셜로그인을 했었는지 확인
            user = User.objects.get(social_login_id=user["id"])
            user.last_login = timezone.now()
            user.save()
            refresh_token, access_token = get_tokens_for_user(user)
            expires_at = (
                timezone.now()
                + getattr(settings, "SIMPLE_JWT", None)["ACCESS_TOKEN_LIFETIME"]
            )
            if self.user.profile.image:
                image = S3_BASE_URL + str(self.user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt토큰, 이름, 타입 프론트엔드에 전달
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
                name=user["properties"]["nickname"],  # kakao는 닉네임만 전달됨
                social_platform="kakao",
                email=user["properties"].get("email", None),
                last_login=timezone.now(),
            )
            user.save()

            refresh_token, access_token = get_tokens_for_user(user)
            if self.user.profile.image:
                image = S3_BASE_URL + str(self.user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt토큰, 이름, 타입 프론트엔드에 전달
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


class NaverLoginView(View):  # 네이버 로그인
    def post(self, request):
        data = json.loads(request.body)
        access_token = data.get("key", None)
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://openapi.naver.com/v1/nid/me"  # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 네이버 API 주소
        response = requests.request(
            "GET", url, headers=headers
        )  # API를 요청하여 회원의 정보를 response에 저장
        user = response.json()

        if User.objects.filter(email=user["response"]["email"]).exists():
            return JsonResponse({"detail": "The email already exits"}, status=400)

        elif User.objects.filter(
            social_login_id=user["response"]["id"], social_platform="naver"
        ).exists():  # 기존에 소셜로그인을 했었는지 확인
            user = User.objects.get(social_login_id=user["response"]["id"])
            user.last_login = timezone.now()
            user.save()
            refresh_token, access_token = get_tokens_for_user(user)
            if self.user.profile.image:
                image = S3_BASE_URL + str(self.user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt토큰, 이름, 타입 프론트엔드에 전달
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
            if self.user.profile.image:
                image = S3_BASE_URL + str(self.user.profile.image)
            else:
                image = None
            return JsonResponse(
                {  # jwt토큰, 이름, 타입 프론트엔드에 전달
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
            {  # jwt토큰, 이름, 타입 프론트엔드에 전달
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
