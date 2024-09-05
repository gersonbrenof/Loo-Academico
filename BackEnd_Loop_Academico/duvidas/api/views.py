from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from duvidas.models import Duvidas
from duvidas.api.serializers import DuvidasSerializer, DuvidasExbirSerializer


class DuvidasViewSet(viewsets.ModelViewSet):
    queryset = Duvidas.objects.all()
    serializer_class = DuvidasSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def perform_create(self, serializer):
        anonimo = serializer.validated_data.get('anonimo', True)
        serializer.save(usuario=self.request.user.aluno, anonimo=anonimo)
        
class ExibirDuvidasView(generics.ListAPIView):
    serializer_class = DuvidasExbirSerializer
    permission_classes = [IsAuthenticated]  # Garante que apenas usuários autenticados acessem a view

    def get_queryset(self):
        # Filtra as dúvidas para o aluno logado
        usuario_logado = self.request.user.aluno  # Supondo que Aluno esteja relacionado com User
        return Duvidas.objects.filter(aluno=usuario_logado)