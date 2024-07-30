from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from contas.models import Aluno, Perfil
from contas.api.serializers import UserCreateSerializer,AlunoSerializer, PerfilSerializer, AtualizarFotoPerfilSerializer, LoginSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
# View para registro do aluno


class AlunoRegisterAPI(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Aluno.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save()

# Função para login do aluno
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                user = Aluno.objects.get(email=email)
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
                else:
                    return Response({"detail": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            except Aluno.DoesNotExist:
                return Response({"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ViewSet para Perfil do aluno
class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    http_method_names = ['get', 'put']
    permission_classes = [IsAuthenticated]

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