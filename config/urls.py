from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("users.urls")),
    path("api/v1/mypage/", include("mypage.urls")),
]
