from rest_framework import serializers
from turma.models import Turma


class ValidarCodicoTurmaSerializer(serializers.Serializer):
    codicoTurma = serializers.CharField()

    def validate_codicoTurma(self, value):
        if not Turma.objects.filter(codicoTurma=value).exists():
            raise serializers.ValidationError('Código da turma é inválido, tente novamente.')
        return value