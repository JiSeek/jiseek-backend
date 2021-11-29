from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("users.urls")),
    path("api/v1/mypage/", include("mypage.urls")),
    path("api/v1/boards/", include("boards.urls")),
    path("api/v1/foods/", include("foods.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
