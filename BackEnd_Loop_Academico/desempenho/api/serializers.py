from rest_framework import serializers
from desempenho.models import Desempenho
class DesempenhoSerializer(serializers.ModelSerializer):
    porcentagem_desempenho = serializers.ReadOnlyField()
    status_avaliacao = serializers.ReadOnlyField()

    class Meta:
        model = Desempenho
        fields = [
            'id',
            'aluno',
            'turma',
            'pontuacaoAluno',
            'data_criacao',
            'tentativas',
            'status',
            'observacao',
            'avaliacao',
            'total_respostas',
            'respostas_corretas',
            'porcentagem_desempenho',
            'status_avaliacao',
        ]