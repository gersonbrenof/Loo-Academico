from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from duvidas.models import Duvidas
from duvidas.api.serializers import DuvidasSerializer


class DuvidasViewSet(viewsets.ModelViewSet):
    queryset = Duvidas.objects.all()
    serializer_class = DuvidasSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        anonimo = serializer.validated_data.get('anonimo', True)
        serializer.save(usuario=self.request.user.aluno, anonimo=anonimo)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Duvidas.objects.all()
        return Duvidas.objects.filter(aluno=self.request.user.aluno)