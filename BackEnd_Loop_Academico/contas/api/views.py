from rest_framework.response import Response
from rest_framework import viewsets, status, generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from contas.models import Aluno, Perfil
from contas.api.serializers import (
    UserCreateSerializer,
    AlunoSerializer,
    UserSerializer,
    PerfilSerializer,
    AtualizarFotoPerfilSerializer,
    LoginSerializer
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, Token

# View para registro do aluno
class AlunoRegisterAPI(generics.CreateAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            aluno = serializer.save()
            # Cria um token para o usuário após o cadastro
            user = aluno.user
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Função para login do aluno
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ViewSet para Perfil do aluno
class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    http_method_names = ['get', 'put']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Obtém o usuário autenticado
        user = self.request.user

        # Busca o aluno associado ao usuário
        try:
            aluno = Aluno.objects.get(user=user)
        except Aluno.DoesNotExist:
            return Perfil.objects.none()  # Se não encontrar o aluno, retorna um queryset vazio

        # Filtra os perfis pelo aluno
        return Perfil.objects.filter(aluno=aluno)

# View para atualizar a foto de perfil
class AtualizarFotoPerfilView(generics.UpdateAPIView):
    queryset = Perfil.objects.all()
    serializer_class = AtualizarFotoPerfilSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PerfilSerializer
        return AtualizarFotoPerfilSerializer

    def perform_update(self, serializer):
        perfil = self.get_object()
        if perfil.aluno != self.request.user:
            raise PermissionDenied("Você não tem permissão para atualizar este perfil.")
        serializer.save()

# View protegida para testes
class ProtectedView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "This is a protected endpoint"}, status=status.HTTP_200_OK)
