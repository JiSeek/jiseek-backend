from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from boards.models import Board
from .serializers import BoardSerializer


class BoardPagination(PageNumberPagination):
    page_size = 9


class BoardsView(APIView):
    def get(self, request):
        boards = Board.objects.all()
        paginator = BoardPagination()
        results = paginator.paginate_queryset(boards, request)
        serializer = BoardSerializer(results, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save(user=request.user)
            board_serializer = BoardSerializer(board)
            return Response(data=board_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardView(APIView):
    def get_board(self, pk):
        try:
            board = Board.objects.get(pk=pk)
            return board
        except Board.DoesNotExist:
            return None

    def get(self, request, pk):
        board = self.get_board(pk)
        if board:
            serializer = BoardSerializer(board)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
