from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers.login_serializer import LoginSerializer
from users.serializers.register_user_serializer import RegisterUserSerializer
from users.services.user_service import UserService


class UserViewSet(viewsets.ViewSet):

    def get_permissions(self):

        if self.action in ["login", "create"]:
            return [AllowAny()]

        return super().get_permissions()

    @action(detail=False, methods=["post"])
    def login(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        dto = serializer.to_dto()

        result = UserService.login(dto)

        return Response(
            result,
            status=status.HTTP_200_OK
        )

    def create(self, request):

        serializer = RegisterUserSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        dto = serializer.to_dto()

        result = UserService.create_user(
            dto
        )

        return Response(result, status=status.HTTP_201_CREATED)