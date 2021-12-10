from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from boards.models import Board, Comment
from .serializers import BoardSerializer, BoardsSerializer, CommentSerializer
from .permissions import IsSelfOrReadOnly


class BoardPagination(PageNumberPagination):
    page_size = 24


class BoardsRankView(ListAPIView):
    """
    좋아요 갯수를 기준으로 상위 9개의 글을 제공
    -----
    """

    queryset = Board.objects.order_by("-count")[:9]
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BoardsView(ListCreateAPIView):
    """
    게시글 전체 조회, 작성
    -----
    """

    queryset = Board.objects.all()
    serializer_class = BoardsSerializer
    pagination_class = BoardPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    """
    게시글 조회, 수정, 삭제
    -----
    """

    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsSelfOrReadOnly]
        return [permission() for permission in permission_classes]


class CommentsView(ListCreateAPIView):
    """
    댓글 조회, 작성
    -----
    """

    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsSelfOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        comments = Comment.objects.filter(board__id=pk).order_by("-created")
        return comments

    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        serializer.save(user=self.request.user, board=Board.objects.get(pk=pk))


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
        """
        댓글 조회, 수정, 삭제
        -----
        댓글 아이디를 기반으로 특정 댓글 조회
        """
        comment = self.get_comment(board_pk, comment_pk)
        if comment:
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, board_pk, comment_pk):
        """
        댓글 조회, 수정, 삭제
        -----
        댓글 아이디를 기반으로 특정 댓글 수정
        """
        comment = self.get_comment(board_pk, comment_pk)

        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, board_pk, comment_pk):
        """
        댓글 조회, 수정, 삭제
        -----
        댓글 아이디를 기반으로 특정 댓글  삭제
        """
        comment = self.get_comment(board_pk, comment_pk)
        comment.delete()
        return Response({"message": "Comment has been deleted!"})
