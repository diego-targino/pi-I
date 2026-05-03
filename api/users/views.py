<<<<<<< HEAD
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile


@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ViewSet):

    # 🔐 LOGIN
    @action(detail=False, methods=['post'])
    def login(self, request):
        telefone = request.data.get('telefone')
        senha = request.data.get('password')

        if not telefone or not senha:
            return Response({'error': 'Telefone e senha são obrigatórios'}, status=400)

        try:
            User.objects.get(username=telefone)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não cadastrado'}, status=404)

        user = authenticate(request, username=telefone, password=senha)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login realizado com sucesso'})
        else:
            return Response({'error': 'Telefone ou senha incorretos'}, status=400)

    # 🧾 CADASTRO COMPLETO (RF001)
    @action(detail=False, methods=['post'])
    def register(self, request):
        nome = request.data.get('nome')
        telefone = request.data.get('telefone')
        senha = request.data.get('password')

        estado = request.data.get('estado')
        cidade = request.data.get('cidade')
        localidade = request.data.get('localidade')
        fazenda = request.data.get('fazenda')

        # validação obrigatória
        if not nome or not telefone or not senha:
            return Response({'error': 'Nome, telefone e senha são obrigatórios'}, status=400)

        # telefone já cadastrado
        if User.objects.filter(username=telefone).exists():
            return Response({'error': 'Telefone já cadastrado'}, status=400)

        # cria usuário
        user = User.objects.create_user(
            username=telefone,
            password=senha
        )

        # cria perfil
        Profile.objects.create(
            user=user,
            nome=nome,
            telefone=telefone,
            estado=estado or '',
            cidade=cidade or '',
            localidade=localidade or '',
            fazenda=fazenda or ''
        )

        return Response({'message': 'Cadastro realizado com sucesso'})
=======
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer
from users.services import UserService

class UserViewSet(ViewSet):

    def create(self, request):
        user = UserService.create_user(request.data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
>>>>>>> a25b68c5809fd1d7ab5a6636f44fb6e370397478
