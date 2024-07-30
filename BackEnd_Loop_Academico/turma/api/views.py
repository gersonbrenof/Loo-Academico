from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets,  serializers
from contas.models import Aluno
from rest_framework.views import APIView
from .serializers import VincularTurmaSerializer, Turma
from rest_framework.permissions import IsAuthenticated
from contas.models import Perfil
from django.http import Http404
from rest_framework import generics, permissions
from django.core.exceptions import PermissionDenied

class AtualizarMinhaTurmaView(generics.UpdateAPIView):
    serializer_class = VincularTurmaSerializer
    permission_classes = [IsAuthenticated]  # Assegure-se de que o usuário está autenticado

    def get_object(self):
        # Obtém o aluno logado
        user = self.request.user
        try:
            aluno = Aluno.objects.get(email=user.email)
        except Aluno.DoesNotExist:
            raise  PermissionDenied("Usuário não associado a um aluno.")
        return aluno
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
   