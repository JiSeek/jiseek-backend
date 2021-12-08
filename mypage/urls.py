from django.urls import path
from . import views


urlpatterns = [
    path("board-favs/", views.BoardFavsAPI.as_view()),
    path("myboards/", views.MyBoardsAPI.as_view()),
    path("food-favs/", views.FoodFavsAPI.as_view()),
    path("board/like/<int:pk>/", views.like_board),
    path("food/like/<int:pk>/", views.like_food),
]
