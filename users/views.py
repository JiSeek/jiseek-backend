from django.contrib.auth import get_user_model
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
import jwt, requests, datetime

User = get_user_model()
SECRET_KEY = "secret_key"


class GoogleLoginView(View):
    # 소셜로그인을 하면 User테이블에 아이디와 패스워드를 담아두고

    def get(self, request):  # id_token만 이용해 헤더로 받기
        token = request.headers[
            "Authorization"
        ]  # 프론트엔드에서 HTTP로 들어온 헤더에서 id_token(Authorization)을 변수에 저장
        url = "https://oauth2.googleapis.com/tokeninfo?id_token="  # 토큰을 이용해서 회원의 정보를 확인하기 위한 google api주소
        response = requests.get(url + token)  # 구글에 id_token을 보내 디코딩 요청
        user = response.json()  # 유저의 정보를 json화해서 변수에 저장

        # user['sub']은 user의 고유 번호
        if User.objects.filter(
            social_login_id=user["sub"], social_platform="kakao"
        ).exists():  # 기존에 가입했었는지 확인
            user_info = User.objects.get(social_login_id=user["sub"])  # 가입된 데이터를 변수에 저장
            user_info.last_login = timezone.now()
            user_info.save()
            encoded_jwt = jwt.encode(
                {"id": user["sub"]}, SECRET_KEY, algorithm="HS256"
            )  # jwt토큰 발행
            none_member_type = 1

            return JsonResponse(
                {  # 프론트엔드에게 access token과 필요한 데이터 전달
                    "access_token": encoded_jwt,
                    "user_name": user["name"],
                    "user_type": none_member_type,
                    "user_pk": user_info.id,
                },
                status=200,
            )
        else:
            new_user_info = User(  # 처음으로 소셜로그인을 했을 경우 회원 정보를 저장(email이 없을 수도 있다 하여, 있으면 저장하고, 없으면 None으로 표기)
                social_login_id=user["sub"],
                name=user["name"],
                social_platform="google",
                email=user.get("email", None),
                last_login=timezone.now(),
            )
            new_user_info.save()  # DB에 저장
            encoded_jwt = jwt.encode(
                {"id": new_user_info.id}, SECRET_KEY, algorithm="HS256"
            )  # jwt토큰 발행

            return JsonResponse(
                {  # DB에 저장된 회원의 정보를 access token과 같이 프론트엔드에 전달
                    "access_token": encoded_jwt,
                    "user_name": new_user_info.name,
                    "user_type": none_member_type,
                    "user_pk": new_user_info.id,
                },
                status=200,
            )


class KakaoLoginView(View):  # 카카오 로그인
    def get(self, request):  # 프론트로부터 전달받은 access_token으로 사용자 정보 가져오기
        access_token = request.headers["Authorization"]
        headers = {
            "Authorization": f"{access_token}",
        }
        url = "https://kapi.kakao.com/v2/user/me"  # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 카카오 API 주소
        response = requests.request(
            "GET", url, headers=headers
        )  # API를 요청하여 회원의 정보를 response에 저장
        user = response.json()
        print("user", user)

        if User.objects.filter(
            social_login_id=user["id"], social_platform="kakao"
        ).exists():  # 기존에 소셜로그인을 했었는지 확인
            user_info = User.objects.get(social_login_id=user["id"])
            user_info.last_login = timezone.now()
            user_info.save()
            encoded_jwt = jwt.encode(
                {"id": user_info.id}, SECRET_KEY, algorithm="HS256"
            )  # jwt토큰 발행

            return JsonResponse(
                {  # jwt토큰, 이름, 타입 프론트엔드에 전달
                    "access_token": encoded_jwt,
                    "user_name": user_info.name,
                    "user_pk": user_info.id,
                },
                status=200,
            )
        else:
            new_user_info = User(
                social_login_id=user["id"],
                name=user["properties"]["nickname"],  # kakao는 닉네임만 전달됨
                social_platform="kakao",
                email=user["properties"].get("email", None),
                last_login=timezone.now(),
            )
            new_user_info.save()
            encoded_jwt = jwt.encode(
                {"id": new_user_info.id}, SECRET_KEY, algorithm="HS256"
            )  # jwt토큰 발행
            return JsonResponse(
                {
                    "access_token": encoded_jwt,
                    "user_name": new_user_info.name,
                    "user_pk": new_user_info.id,
                },
                status=200,
            )


class NaverLoginView(View):  # 네이버 로그인
    def get(self, request):
        access_token = request.headers["Authorization"]
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://openapi.naver.com/v1/nid/me"  # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 네이버 API 주소
        response = requests.request(
            "GET", url, headers=headers
        )  # API를 요청하여 회원의 정보를 response에 저장
        user = response.json()

        if User.objects.filter(
            social_login_id=user["id"], social_platform="naver"
        ).exists():  # 기존에 소셜로그인을 했었는지 확인
            user_info = User.objects.get(social_login_id=user["id"])
            user_info.last_login = timezone.now()
            user_info.save()
            encoded_jwt = jwt.encode(
                {"id": user_info.id}, SECRET_KEY, algorithm="HS256"
            )  # jwt토큰 발행

            return JsonResponse(
                {  # jwt토큰, 이름, 타입 프론트엔드에 전달
                    "access_token": encoded_jwt,
                    "user_name": user_info.nickname,
                    "user_pk": user_info.id,
                },
                status=200,
            )
        else:
            new_user_info = User(
                social_login_id=user["id"],
                name=user["nickname"],
                social_platform="naver",
                email=user["email"],
                last_login=timezone.now(),
            )
            new_user_info.save()
            encoded_jwt = jwt.encode(
                {"id": new_user_info.id}, SECRET_KEY, algorithm="HS256"
            )  # jwt토큰 발행
            return JsonResponse(
                {
                    "access_token": encoded_jwt,
                    "user_name": new_user_info.name,
                    "user_pk": new_user_info.id,
                },
                status=200,
            )
