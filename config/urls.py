from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


docs_view = get_schema_view(
    openapi.Info(
        title="Jiseek API",
        default_version="v1",
        description="""
        지식 Open API 문서 페이지입니다.

        한식을 사진으로 검색하고 공유하는 서비스입니다.

        팀원: 고예림, 고정현, 김지훈, 박지윤, 이민영, 전진성
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="image2jiseek@gmail.com"),
    ),
    permission_classes=(AllowAny,),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("users.urls")),
    path("api/v1/mypage/", include("mypage.urls")),
    path("api/v1/boards/", include("boards.urls")),
    path("api/v1/foods/", include("foods.urls")),
    path("api/v1/search/", include("search.urls")),
    re_path(
        r"^docs/$", docs_view.with_ui("redoc", cache_timeout=0), name="schema-docs"
    ),
    re_path(
        r"^swagger/$",
        docs_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        docs_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
