from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer
from users.services import UserService

class UserViewSet(ViewSet):

    def create(self, request):
        user = UserService.create_user(request.data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)