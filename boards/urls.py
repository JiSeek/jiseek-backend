from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [
    path("", views.BoardsView.as_view()),
    path("<int:pk>/", views.BoardView.as_view()),
    path("<int:pk>/comments/", views.CommentsView.as_view()),
    path("<int:board_pk>/comments/<int:comment_pk>", views.CommentView.as_view()),
]
