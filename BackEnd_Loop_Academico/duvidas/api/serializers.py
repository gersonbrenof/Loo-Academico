from rest_framework import serializers
from duvidas.models import Duvidas

class DuvidasExbirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duvidas
        fields = ['id', 'titulo',  'data_criacao', 'status_resposta']
class DuvidasSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nomeAluno', read_only=True, default="Anônimo")
    
    class Meta:
        model = Duvidas
        fields = ['id', 'titulo', 'duvidaAluno', 'data_criacao', 'tematica', 'aluno_nome', 'anonimo']
        extra_kwargs = {
            'aluno': {'write_only': True},  # Define o campo 'aluno' como somente para escrita, para controle interno
            'anonimo': {'required': False}  # Permite que 'anonimo' seja opcional no input
        }

    def create(self, validated_data):
        # Obtém o usuário logado do contexto da requisição
        request = self.context.get('request')
        aluno = getattr(request.user, 'aluno', None) 
        
        # Define o aluno e anônimo nos dados validados
        validated_data['aluno'] = aluno
        return super().create(validated_data)