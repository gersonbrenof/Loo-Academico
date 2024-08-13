from rest_framework import serializers
from duvidas.models import Duvidas

class DuvidasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duvidas
        fields = ['id', 'titulo', 'duvidaAluno', 'data_criacao', 'status_resposta', 'tematica', 'aluno',    'anonimo']
    
    aluno_nome = serializers.CharField(source ='aluno.nomeAluno', read_only= True, default = "Anônimo" )

    class Meta:
        model = Duvidas
        fields = ['id', 'titulo', 'duvidaAluno', 'data_criacao', 'status_resposta', 'tematica','aluno' , 'anonimo', 'aluno_nome']

    def create(self, validated_data):
        # verificar se a duvida e anonimo e define o campo aluo corretamente
        anonimo = validated_data.pop('anonimo', True)
        usuario = self.context['request'].user.aluno if not anonimo else None
        validated_data['aluno'] = usuario
        return super().create(validated_data)