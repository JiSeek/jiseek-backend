from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "search"

urlpatterns = [
    path("", views.SearchImageView.as_view()),
    path("<int:pk>/", views.SearchResultView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
