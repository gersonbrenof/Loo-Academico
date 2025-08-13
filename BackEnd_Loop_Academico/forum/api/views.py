from rest_framework import viewsets, permissions
from rest_framework import generics, mixins, permissions

from forum.models import Forum, ResponderTopico
from forum.api.serializers import ForumSerializer, ResponderTopicoSerializer, ForumExibirSerializer, ExibirResponderTopicoSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class ForumExibirViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumExibirSerializer
    permission_classes = [IsAuthenticated]

    # Se quiser só permitir GET (list/retrieve)
    http_method_names = ['get']

class ForumViewSet(viewsets.ModelViewSet):
    """
    Cria ou edita fóruns associando automaticamente o aluno logado.
    """
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        aluno = self.request.user.aluno
        serializer.save(aluno=aluno)


class ResponderTopicoListCreateView(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExibirResponderTopicoSerializer
        return ResponderTopicoSerializer

    def get_queryset(self):
        forum_id = self.kwargs.get('forum_id')
        return ResponderTopico.objects.filter(forum_id=forum_id)

    def perform_create(self, serializer):
        aluno = self.request.user.aluno
        forum_id = self.kwargs.get('forum_id')
        forum = Forum.objects.get(pk=forum_id)
        serializer.save(aluno=aluno, forum=forum)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)