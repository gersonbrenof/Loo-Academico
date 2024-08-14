from rest_framework import serializers
from exercicio.models import Exercicio, ListaExercicio, Sintaxe, Problema, DiscricaoDetalhada, DicaAluno, ResponderExercicio

class ExercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercicio
        fields = ['id', 'titulo', 'descricao', 'data_criacao', 'status', 'numeroDoExercicio', 'entradaExemplo', 'saidaExemplo']



class ListaExercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaExercicio
        fields = ['id', 'tiltulo', 'numeroExercicio', 'dataCriacao', 'status', 'dificuldade', 'totalExercicio']

class ResponderExercicioSerializer(serializers.ModelSerializer):
    exercicio = serializers.PrimaryKeyRelatedField(queryset=Exercicio.objects.all(), required=True)
    aluno = serializers.HiddenField(default =serializers.CurrentUserDefault())
    class Meta:
        model = ResponderExercicio
        fields = ['id', 'exercicio', 'aluno', 'resultado', 'codigoDoExercicio', 'pontuacao', 'dataEnvio']
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


class DicaAluno(serializers.ModelSerializer):
    discricaoDetalhada = DiscricaoDetalhadaSerializer(read_only=True)
    sintaxe = SintaxeSerializer(read_only = True)
    problema = ProblemaSerilizer(read_only = True)
    exercicio = ExercicioSerializer(read_only = True)
    class Meta:
        model = DicaAluno
        fields = ['id', 'codigoApoio', 'descricaoDetalhada', 'sintaxe', 'problema', 'exercicio']