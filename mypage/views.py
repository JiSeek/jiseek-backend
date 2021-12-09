from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.jwt_auth import JWTCookieAuthentication  # will be removed
from .serializers import BoardFavsSerializer, FoodFavsSerializer, MyBoardsSerializer
from .models import Profile
from boards.models import Board
from foods.models import Food

User = get_user_model()


class BoardFavsAPI(generics.ListAPIView):
    """
    게시글 좋아요 목록 조회
    """

    serializer_class = BoardFavsSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        user = self.request.user
        profile_id = Profile.objects.get(user=user).id
        liked_boards = Profile.board_favs.through.objects.filter(
            profile_id=profile_id
        ).all()
        board_ids = [liked_board.id for liked_board in liked_boards]

        return Board.objects.filter(id__in=board_ids).all()


class FoodFavsAPI(generics.ListAPIView):
    """
    음식 좋아요 목록 조회
    """

    serializer_class = FoodFavsSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        user = self.request.user
        profile_id = Profile.objects.get(user=user).id
        liked_foods = Profile.food_favs.through.objects.filter(
            profile_id=profile_id
        ).all()
        food_ids = [liked_food.id for liked_food in liked_foods]

        return Food.objects.filter(id__in=food_ids).all()


class MyBoardsAPI(generics.ListAPIView):
    """
    내가 쓴 게시물 목록 조회
    """

    serializer_class = MyBoardsSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        user = self.request.user
        boards = Board.objects.filter(user=user).all()
        return boards


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def like_board(request, pk):
    """
    게시글 좋아요 목록에 추가/삭제
    """
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user_id=user_id)
    board = Board.objects.get(pk=pk)

    if profile and board:
        if user in board.like_users.all():
            board.like_users.remove(user)
            board.count -= 1
            board.save()
        else:
            board.like_users.add(user)
            board.count += 1
            board.save()
        if board in profile.board_favs.all():
            profile.board_favs.remove(board)
            return Response("Removed")
        else:
            profile.board_favs.add(board)
            return Response("Added")
    else:
        return Response("Unsuccessful", status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def like_food(request, pk):
    """
    음식 좋아요 목록에 추가/삭제
    """
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    food = Food.objects.get(pk=pk)

    if profile and food:
        if food in profile.food_favs.all():
            profile.food_favs.remove(food)
            return Response("Removed")
        else:
            profile.food_favs.add(food)
            return Response("Added")
    else:
        return Response("Unsuccessful", status.HTTP_404_NOT_FOUND)
