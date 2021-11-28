from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "boards"

urlpatterns = [
    path("", views.BoardsView.as_view()),
    path("<int:pk>/", views.BoardView.as_view()),
    path("<int:pk>/comments/", views.CommentsView.as_view()),
    path("<int:board_pk>/comments/<int:comment_pk>", views.CommentView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
