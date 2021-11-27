from django.urls import path, re_path, include
from django.conf.urls.static import static
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView

# from allauth.account.views import confirm_email

from . import views
from config import settings


urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("register/", include("dj_rest_auth.registration.urls")),
    path("logout-all/", views.LogoutView.as_view()),
    path("info/", views.UserInfoView.as_view()),
    path("access-token/refresh/", views.CustomTokenRefreshView.as_view()),
    path("custom/login/", views.CustomLoginView.as_view()),
    path("login/google/", views.GoogleLoginView.as_view()),
    path("login/kakao/", views.KakaoLoginView.as_view()),
    path("login/naver/", views.NaverLoginView.as_view()),
    # re_path(
    #     r"^verify/email?code=(?P<key>\w+)/$",
    #     confirm_email,
    #     name="account_confirm_email",
    # ),
    re_path(
        r"^account-confirm-email/",
        views.CustomVerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
]
