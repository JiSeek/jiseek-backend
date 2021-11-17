from django.urls import path
from . import views

app_name = "boards"

urlpatterns = [
    path("", views.BoardsView.as_view()),
    path("<int:pk>/", views.BoardView.as_view()),
]
