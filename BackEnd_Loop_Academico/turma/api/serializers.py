from rest_framework import serializers
from turma.models import Turma
from contas.models import Aluno

class VincularTurmaSerializer(serializers.ModelSerializer):
    codicoTurma = serializers.CharField(write_only=True)  # Campo extra para entrada de dados

    class Meta:
        model = Aluno
        fields = ['codicoTurma']  # Inclua codicoTurma nos fields

    def validate_codicoTurma(self, value):
        # Verifica se o código da turma existe no banco de dados
        if not Turma.objects.filter(codicoTurma=value).exists():
            raise serializers.ValidationError("Código de turma inválido.")
        return value

    def update(self, instance, validated_data):
        # Busca a turma pelo código correto
        turma = Turma.objects.get(codicoTurma=validated_data['codicoTurma'])
        instance.turma = turma  # Atribui a turma ao aluno
        instance.save()  # Salva a instância do aluno
        return instance
