from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.jwt_auth import JWTCookieAuthentication  # will be removed
from .serializers import (
    BoardFavsSerializer,
    FoodFavsSerializer,
    UpdateUserSerializer,
)
from boards.serializers import BoardSerializer
from .models import Profile
from boards.models import Board
from foods.models import Food

User = get_user_model()


class BoardFavsAPI(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = BoardFavsSerializer
    authentication_classes = [
        JWTCookieAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]


class FoodFavsAPI(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = FoodFavsSerializer
    authentication_classes = [
        JWTCookieAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]


class ProfileAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    authentication_classes = [
        JWTCookieAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def like_board(request, pk):
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    board = Board.objects.get(pk=pk)

    if profile and board:
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
