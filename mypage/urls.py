from django.urls import path, include
from django.conf.urls.static import static
from . import views
from config import settings

urlpatterns = [
    path("", views.ProfileAPI.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
