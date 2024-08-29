from rest_framework import viewsets, permissions
from forum.models import Forum, ResponderTopico
from forum.api.serializers import ForumSerializer, ResponderTopicoSerializer, ForumExibirSerilizer, ExibirResponderTopicoSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

class ForumExibirViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumExibirSerilizer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Forum.objects.all()
class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        # Associa automaticamente o aluno logado ao fórum
        aluno = self.request.user.aluno
        serializer.save(aluno=aluno)
    
class ResponderTopicoViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        # Retorna o serializer apropriado com base no método da solicitação
        if self.request.method == 'GET':
            return ExibirResponderTopicoSerializer
        return ResponderTopicoSerializer

    def get_queryset(self):
        forum_id = self.kwargs.get('forum_id')
        if forum_id:
            return ResponderTopico.objects.filter(forum_id=forum_id)
        return ResponderTopico.objects.all()

    def perform_create(self, serializer):
        aluno = self.request.user.aluno
        forum_id = self.kwargs.get('forum_id')
        forum = Forum.objects.get(id=forum_id)
        serializer.save(aluno=aluno, forum=forum)
