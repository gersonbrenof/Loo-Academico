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
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            aluno = Aluno.objects.get(email=user.email)
        except Aluno.DoesNotExist:
            raise PermissionDenied("Usuário não associado a um aluno.")
        return aluno

    def patch(self, request, *args, **kwargs):
        aluno = self.get_object()

        # Verifica se o aluno já está associado a uma turma
        if aluno.turma:
            return Response({"detail": f"O aluno já está associado à turma {aluno.turma.codicoTurma}"}, status=status.HTTP_400_BAD_REQUEST)

        # Atualiza a turma do aluno
        serializer = self.get_serializer(aluno, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "detail": "Aluno associado à turma com sucesso"}, status=status.HTTP_200_OK)
        
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class VerificarAssociacaoTurmaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            aluno = Aluno.objects.get(email=user.email)
        except Aluno.DoesNotExist:
            raise PermissionDenied("Usuário não associado a um aluno.")
        
        if aluno.turma:
            return Response({"detail": f"O aluno já está associado à turma {aluno.turma.codicoTurma}"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "O aluno não está associado a nenhuma turma."}, status=status.HTTP_200_OK)