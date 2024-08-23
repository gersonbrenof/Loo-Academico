from rest_framework import serializers
from forum.models import Forum, ResponderTopico
class ForumExibirSerilizer(serializers.ModelSerializer):
    class Meta:
         model = Forum
         fields = ['id', 'titulo', 'descricao','data_inico', 'categoria','aluno']


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id', 'titulo', 'descricao','data_inico', 'categoria']
    
class ResponderTopicoSerializer(serializers.ModelSerializer):
    forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all(), required=True)
    forumdetalhe = ForumSerializer(source='forum',read_only=True)
    class Meta:
        model = ResponderTopico
        fields = ['id', 'forum', 'forumdetalhe', 'respostaForum', 'data_resposta', 'aluno']