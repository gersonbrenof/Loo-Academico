from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets,  serializers
from contas.models import Aluno
from rest_framework.views import APIView
from .serializers import VincularTurmaSerializer, Turma
from rest_framework.permissions import IsAuthenticated
from contas.models import Perfil
from django.http import Http404
from rest_framework import generics


class AtualizarMinhaTurmaView(generics.UpdateAPIView):
    serializer_class = VincularTurmaSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Obtém o aluno logado
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
   