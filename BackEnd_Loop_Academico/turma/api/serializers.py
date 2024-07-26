from rest_framework import serializers
from turma.models import Turma
from contas.models import Aluno

class VincularTurmaSerializer(serializers.ModelSerializer):
    codicoTurma = serializers.CharField(write_only=True)

    class Meta:
        model = Aluno
        fields = ['codicoTurma']

    def validate_codicoTurma(self, value):
        if not Turma.objects.filter(codicoTurma=value).exists():
            raise serializers.ValidationError("O código da turma não existe.")
        return value

    def update(self, instance, validated_data):
        turma_codigo = validated_data.get('codicoTurma')
        turma = Turma.objects.get(codicoTurma=turma_codigo)
        instance.turma = turma
        instance.save()
        return instance