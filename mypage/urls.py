from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views
from config import settings


urlpatterns = [
    path("board-favs/", views.BoardFavsAPI.as_view()),
    path("food-favs/", views.FoodFavsAPI.as_view()),
    path("profile/", views.ProfileAPI.as_view()),
    path("board/like/<int:pk>/", views.like_board),
    path("food/like/<int:pk>/", views.like_food),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
