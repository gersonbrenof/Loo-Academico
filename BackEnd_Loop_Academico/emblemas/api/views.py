from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from emblemas.models import Emblema
from emblemas.api.serializers import EmblemaSerializer

#Lsita os embelma do aluno
class ListaEmblemaALunoView(generics.ListAPIView):
    serializer_class = EmblemaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        aluno = self.request.user.aluno
        return Emblema.objects.filter(aluno=aluno)


class ListaTodosEmblemasView(generics.ListAPIView):
    serializer_class = EmblemaSerializer
    permission_classes = [IsAuthenticated]
    queryset = Emblema.objects.all()
    def get_queryset(self):
        aluno = self.request.user.aluno
        return Emblema.objects.filter(aluno=aluno)
    
class DesbloquearEmblemaView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        aluno = self.request.user.aluno
        criterio = request.data.get('criterio')

        # verificar se o aluno ja tem o embelma com o criterio
        if Emblema.objects.filter(aluno=aluno, criterio=criterio).exists():
            return Response({"detail": "O aluno já possui esse emblema"}, status=status.HTTP_400_BAD_REQUEST)
        # busca um embelma com crietrio especifico
        emblema = Emblema.objects.filter(criterio=criterio).first()
        if emblema:
            return Response({"detail": "Criterio não corresponde a nenhum emblema"}, status=status.HTTP_400_BAD_REQUEST)
        
        emblema.aluno = aluno
        emblema.save()

        return Response({"detail": "emblema desbloqueado com sucesso!"}, status=status.HTTP_200_OK)