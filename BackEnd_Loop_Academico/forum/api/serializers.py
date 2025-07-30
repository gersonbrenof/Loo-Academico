from rest_framework import serializers
from forum.models import Forum, ResponderTopico
from contas.api.serializers import AlunoSerializer
class ForumExibirSerilizer(serializers.ModelSerializer):
    nome_do_aluno = serializers.CharField(source='aluno.nomeAluno', read_only=True)
    foto_perfil = serializers.SerializerMethodField()
    class Meta:
         model = Forum
         fields = ['id', 'titulo', 'descricao','data_inico', 'categoria','nome_do_aluno', 'foto_perfil']

    def get_foto_perfil(self, obj):
        if obj.aluno and hasattr(obj.aluno, 'perfil') and obj.aluno.perfil.fotoPerfil:
            return obj.aluno.perfil.fotoPerfil.url
        return None
class ForumSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.titulo', read_only=True)
    class Meta:
        model = Forum
        fields = ['id', 'titulo', 'descricao','data_inico', 'categoria_nome']
    
class ResponderTopicoSerializer(serializers.ModelSerializer):
    forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all(), required=True)
    forumdetalhe = ForumSerializer(source='forum',read_only=True)
    class Meta:
        model = ResponderTopico
        fields = ['id', 'forum', 'forumdetalhe', 'respostaForum', 'data_resposta',]
class ExibirResponderTopicoSerializer(serializers.ModelSerializer):
    forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all(), required=True)
    forumdetalhe = ForumSerializer(source='forum',read_only=True)
    aluno = AlunoSerializer(read_only=True)
    class Meta:
        model = ResponderTopico
        fields = ['id', 'forum', 'forumdetalhe', 'respostaForum', 'data_resposta', 'aluno']