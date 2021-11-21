from rest_framework.permissions import BasePermission


class IsSelfOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, board):
        return board.user == request.user
