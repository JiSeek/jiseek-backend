from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from search.serializers import SearchImageSerializer, SearchResultSerializer
from .models import SearchImage, SearchResult


class SearchImageView(CreateAPIView):
    queryset = SearchImage.objects.all()
    serializer_class = SearchImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchResultView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SearchResultSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return SearchResult.objects.filter(photo_id=pk)
