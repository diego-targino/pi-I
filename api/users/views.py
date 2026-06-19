from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from users.serializers.login_serializer import LoginSerializer
from users.serializers.register_user_serializer import RegisterUserSerializer
from users.serializers.response_serializers import LoginResponseSerializer, RegisterUserResponseSerializer
from users.services.user_service import UserService


class UserViewSet(viewsets.ViewSet):
    """
    API de Usuários
    
    Endpoints para autenticação e registro de usuários.
    """

    def get_permissions(self):

        if self.action in ["login", "create"]:
            return [AllowAny()]

        return super().get_permissions()

    @extend_schema(
        summary="Fazer Login",
        description="Autentica um usuário com telefone e senha, retornando token JWT",
        request=LoginSerializer,
        responses={
            200: LoginResponseSerializer,
            400: {"description": "Dados inválidos"},
        }
    )
    @action(detail=False, methods=["post"])
    def login(self, request):
        """
        Autentica um usuário.
        
        Retorna um token JWT para uso em requisições subsequentes.
        """
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

    @extend_schema(
        summary="Registrar Novo Usuário",
        description="Cria uma nova conta de usuário com informações pessoais e dados da fazenda",
        request=RegisterUserSerializer,
        responses={
            201: RegisterUserResponseSerializer,
            400: {"description": "Dados inválidos ou usuário já existe"},
        }
    )
    def create(self, request):
        """
        Registra um novo usuário.
        
        Requer nome, telefone, senha e dados da fazenda.
        """
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