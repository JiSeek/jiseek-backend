from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from .models import SearchResult

# Create your views here.
class SearchResultsView(APIView):
    # def get_result(self, pk):
    #     try:
    #         results = SearchResult.objects.filter(pk=pk)
    #         if comment.board.id == board_pk:
    #             return results
    #         else:
    #             return None
    #     except Comment.DoesNotExist:
    #         return None

    # def get(self, request, pk]):
    #     results = self.get_comment(pk)
    #     if comment:
    #         serializer = CommentSerializer(comment)
    #         return Response(serializer.data)
    #     else:
    #         return Response(status=HTTP_404_NOT_FOUND)
