from rest_framework import serializers
from forum.models import Forum, ResponderTopico

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id', 'titulo', 'descricao','data_inico', 'aluno']
    
class ResponderTopicoSerializer(serializers.ModelSerializer):
    forum = ForumSerializer(read_only=True)
    class Meta:
        model = ResponderTopico
        fields = ['id', 'forum', 'respostaForum', 'data_resposta']