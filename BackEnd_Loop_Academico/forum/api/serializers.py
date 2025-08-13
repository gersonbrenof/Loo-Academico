from rest_framework import serializers
from forum.models import Forum, ResponderTopico
from contas.api.serializers import AlunoSerializer

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id', 'titulo', 'descricao', 'data_inico', 'categoria']

class RespostaSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)

    class Meta:
        model = ResponderTopico
        fields = ['id', 'respostaForum', 'data_resposta', 'aluno']

class ResponderTopicoSerializer(serializers.ModelSerializer):
    forumdetalhe = ForumSerializer(source='forum', read_only=True)
    aluno = AlunoSerializer(read_only=True)

    class Meta:
        model = ResponderTopico
        fields = ['id', 'forumdetalhe', 'respostaForum', 'data_resposta', 'aluno']
        read_only_fields = ['forumdetalhe', 'data_resposta', 'aluno']

class ExibirResponderTopicoSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)

    class Meta:
        model = ResponderTopico
        fields = ['id', 'respostaForum', 'data_resposta', 'aluno']

class ForumExibirSerializer(serializers.ModelSerializer):
    nome_do_aluno = serializers.CharField(source='aluno.nomeAluno', read_only=True)
    foto_perfil = serializers.SerializerMethodField()
    respostas = ResponderTopicoSerializer(many=True, read_only=True)  # agora puxa todos os campos

    class Meta:
        model = Forum
        fields = [
            'id',
            'titulo',
            'descricao',
            'data_inico',
            'categoria',
            'nome_do_aluno',
            'foto_perfil',
            'respostas',
        ]

    def get_foto_perfil(self, obj):
        if obj.aluno and hasattr(obj.aluno, 'perfil') and obj.aluno.perfil.fotoPerfil:
            return obj.aluno.perfil.fotoPerfil.url
        return None