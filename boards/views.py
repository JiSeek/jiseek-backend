from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from boards.models import Board
from .serializers import BoardSerializer


class BoardPagination(PageNumberPagination):
    page_size = 9


class BoardsView(ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class BoardView(APIView):
#     def get_board(self, pk):
#         try:
#             board = Board.objects.get(pk=pk)
#             return board
#         except Board.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         board = self.get_board(pk)
#         if board:
#             serializer = BoardSerializer(board)
#             return Response(serializer.data)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)
