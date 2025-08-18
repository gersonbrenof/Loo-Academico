from rest_framework import serializers
from desempenho.models import Desempenho
from exercicio.models import Exercicio, ListaExercicio, ResponderExercicio
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
class ExercicioDesempenhoSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Exercicio
        fields = ['id', 'titulo', 'numeroDoExercicio', 'status']

    def get_status(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 'Não Respondido'

        aluno = getattr(request.user, 'aluno', None)
        if not aluno:
            return 'Não Respondido'

        resposta = ResponderExercicio.objects.filter(aluno=aluno, exercicio=obj).last()
        if resposta:
            # Aqui você pode adaptar a lógica: supondo que resultado armazena "Correto" ou "Incorreto"
            return 'Correto' if resposta.resultado == 'Correto' else 'Incorreto'
        return 'Não Respondido'


class ListaDesempenhoSerializer(serializers.ModelSerializer):
    exercicios = ExercicioDesempenhoSerializer(many=True, read_only=True)

    class Meta:
        model = ListaExercicio
        fields = ['id', 'titulo', 'numeroExercicio', 'dificuldade', 'exercicios']