from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from duvidas.models import Duvidas
from duvidas.api.serializers import DuvidasSerializer, DuvidasExbirSerializer
from django.db.models import Q 
class DuvidasViewSet(viewsets.ModelViewSet):
    queryset = Duvidas.objects.all()
    serializer_class = DuvidasSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']  # Permite apenas o método POST

    def perform_create(self, serializer):
        # Aqui você pode garantir que o aluno esteja associado ao usuário logado
        aluno = getattr(self.request.user, 'aluno', None)
        
        # Certifica-se de que o aluno está associado automaticamente
        serializer.save(aluno=aluno if aluno else None)
        
class ExibirDuvidasView(generics.ListAPIView):
    serializer_class = DuvidasExbirSerializer
    permission_classes = [IsAuthenticated]  # Garante que apenas usuários autenticados acessem a view

    def get_queryset(self):
        usuario_logado = getattr(self.request.user, 'aluno', None)  # Supondo que Aluno esteja relacionado com User
        
        if usuario_logado:
            # Filtra as dúvidas do aluno logado
            return Duvidas.objects.filter(aluno=usuario_logado)
        else:
            # Se não houver um aluno associado ao usuário logado, retorne uma queryset vazia
            return Duvidas.objects.none()