from django.urls import path, re_path, include
from django.conf.urls.static import static
from dj_rest_auth.registration.views import VerifyEmailView

from . import views
from config import settings


urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("register/", include("dj_rest_auth.registration.urls")),
    path("login/google/", views.GoogleLoginView.as_view()),
    path("login/kakao/", views.KakaoLoginView.as_view()),
    path("login/naver/", views.NaverLoginView.as_view()),
    re_path(
        r"^account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
]