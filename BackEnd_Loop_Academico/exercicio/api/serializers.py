from rest_framework import serializers
from exercicio.models import Exercicio, ListaExercicio, Sintaxe, Problema, DiscricaoDetalhada, DicaAluno, ResponderExercicio
from contas.models import Aluno

class ExercicioStatusSerializer(serializers.ModelSerializer):
    
    respondido = serializers.SerializerMethodField()
    class Meta:
      
        model = Exercicio
        fields = ['id','titulo', 'numeroDoExercicio','status','respondido']

    def get_respondido(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 'Nao Respondido'
        try:
            aluno = request.user.aluno
            # Verifica se o exercício foi respondido pelo aluno
            responded = ResponderExercicio.objects.filter(aluno=aluno, exercicio=obj).exists()
            return 'Respondido' if responded else 'Não Respondido'
        except Aluno.DoesNotExist:
            return 'Não Respondido'
        

class ListaExercicioSerializer(serializers.ModelSerializer):
    #exercicios = ExercicioSerializer(many=True, read_only=True)
    total_exercicios = serializers.IntegerField(source = 'toltaExcercicios', read_only = True)
    class Meta:
        model = ListaExercicio
        fields = ['id', 'titulo', 'numeroExercicio', 'dataCriacao', 'dificuldade','total_exercicios']


class ExercicioSerializer(serializers.ModelSerializer):
    lista = ListaExercicioSerializer()
    class Meta:
        
        model = Exercicio
        fields = ['id', 'titulo', 'descricao', 'data_criacao', 'numeroDoExercicio', 'entradaExemplo', 'saidaExemplo','lista']

class ListaExercicioStatusSerilaizer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    total_exercicios = serializers.SerializerMethodField()  # Adicionando o campo calculado
    exercicios = ExercicioStatusSerializer(many=True)

    class Meta:
        model = ListaExercicio
        fields = ['id', 'titulo', 'numeroExercicio', 'dataCriacao', 'dificuldade', 'total_exercicios', 'status', 'exercicios']

    def get_status(self, obj):
        # Verifica se todos os exercícios da lista foram respondidos
        todos_respondidos = all(
            ResponderExercicio.objects.filter(aluno=self.context['request'].user.aluno, exercicio=exercicio).exists()
            for exercicio in obj.exercicios.all()
        )
        if todos_respondidos:
            return 'Indisponível'  # Todos respondidos
        return 'Disponível'  # Pelo menos um não respondido

    def get_total_exercicios(self, obj):
        # Calcula o total de exercícios na lista
        return obj.exercicios.count()

    def update(self, instance, validated_data):
        # Atualizar o status da lista quando necessário
        instance = super().update(instance, validated_data)
        instance.verificar_respostas()  # Chama o método para verificar o status
        return instance
        
class ResponderExercicioSerializer(serializers.ModelSerializer):
    exercicio = serializers.PrimaryKeyRelatedField(queryset=Exercicio.objects.all(), required=True)
    aluno = serializers.HiddenField(default =serializers.CurrentUserDefault())
    class Meta:
        model = ResponderExercicio
        fields = ['id', 'exercicio', 'aluno', 'resultado', 'codigoDoExercicio', 'pontuacao', 'dataEnvio']
        read_only_fields = ['dataEnvio']
class SintaxeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sintaxe
        fields = ['id', 'titulo', 'descricao']

class ProblemaSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Problema
        fields = ['id', 'numeroDica', 'conteudoDica','imagemExemplo']

class DiscricaoDetalhadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscricaoDetalhada
        fields = ['id', 'descricao']


class DicaAlunoSerilizer(serializers.ModelSerializer):
    discricaoDetalhada = DiscricaoDetalhadaSerializer(read_only=True)
    sintaxe = SintaxeSerializer(read_only = True)
    problema = ProblemaSerilizer(read_only = True)
    exercicio = ExercicioSerializer(read_only = True)
    class Meta:
        model = DicaAluno
        fields = ['id', 'codigoApoio', 'discricaoDetalhada', 'sintaxe', 'problema', 'exercicio']