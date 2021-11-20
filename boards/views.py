from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from boards.models import Board, Comment
from .serializers import BoardSerializer, CommentSerializer
from .permissions import IsSelfOrReadOnly


class BoardPagination(PageNumberPagination):
    page_size = 9


class BoardsView(ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BoardView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsSelfOrReadOnly]
        return [permission() for permission in permission_classes]


class CommentsView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(APIView):
    def get_comment(self, board_pk, comment_pk):
        try:
            comment = Comment.objects.get(pk=comment_pk)
            if comment.board.id == board_pk:
                return comment
            else:
                return None
        except Comment.DoesNotExist:
            return None

    def get(self, request, board_pk, comment_pk):
        comment = self.get_comment(board_pk, comment_pk)
        if comment is not None:
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
