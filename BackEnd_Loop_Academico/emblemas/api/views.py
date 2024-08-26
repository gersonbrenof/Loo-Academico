from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from emblemas.models import Emblema
from emblemas.api.serializers import EmblemaSerializer, EmblemaListaTudoSerializer

#Lsita os embelma do aluno
class ListaEmblemaALunoView(generics.ListAPIView):
    serializer_class = EmblemaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        aluno = self.request.user.aluno
        return Emblema.objects.filter(aluno=aluno)


class ListaTodosEmblemasView(generics.ListAPIView):
    serializer_class = EmblemaListaTudoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Emblema.objects.all()

    
class DesbloquearEmblemaView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        aluno = self.request.user.aluno
        criterio = request.data.get('criterio')

        # Verificar se o aluno já tem o emblema com o critério
        if Emblema.objects.filter(aluno=aluno, criterio=criterio).exists():
            return Response({"detail": "O aluno já possui esse emblema"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar um emblema com o critério específico
        emblema = Emblema.objects.filter(criterio=criterio, status='nao_desbloqueado').first()
        if not emblema:
            return Response({"detail": "Critério não corresponde a nenhum emblema"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Atualizar o emblema para o aluno
        emblema.aluno = aluno
        emblema.status = 'desbloqueado'  # Atualizar o status para 'desbloqueado'
        emblema.save()

        return Response({"detail": "Emblema desbloqueado com sucesso!"}, status=status.HTTP_200_OK)