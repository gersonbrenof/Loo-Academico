from rest_framework import viewsets, permissions
from forum.models import Forum, ResponderTopico
from forum.api.serializers import ForumSerializer, ResponderTopicoSerializer


class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    http_method_names = ['get', 'post']
    

class ResponderTopicoViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = ResponderTopico.objects.all()
    serializer_class = ResponderTopicoSerializer
