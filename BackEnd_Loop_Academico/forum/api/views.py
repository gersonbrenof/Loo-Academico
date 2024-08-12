from rest_framework import viewsets, permissions
from forum.models import Forum, ResponderTopico
from forum.api.serializers import ForumSerializer, ResponderTopicoSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        aluno = self.request.user.aluno
        serializer.save(aluno = aluno)
    

class ResponderTopicoViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = ResponderTopico.objects.all()
    serializer_class = ResponderTopicoSerializer

    def perform_create(self, serializer):
        aluno = self.request.user.aluno

        serializer.save(aluno=aluno)
