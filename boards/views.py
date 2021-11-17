from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from boards.models import Board
from .serializers import BoardSerializer
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
