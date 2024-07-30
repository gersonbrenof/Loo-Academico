from rest_framework import serializers
from turma.models import Turma
from contas.models import Aluno

class VincularTurmaSerializer(serializers.ModelSerializer):

    codicoTurma = serializers.CharField()  # Certifique-se de que isso corresponde ao campo esperado

    class Meta:
        model = Aluno
        fields = ['codicoTurma']  # Inclua apenas os campos que existem no modelo Aluno

    def validate_codicoTurma(self, value):
        if not Turma.objects.filter(codigo=value).exists():
            raise serializers.ValidationError("Código de turma inválido.")
        return value

    def update(self, instance, validated_data):
        turma = Turma.objects.get(codigo=validated_data['codicoTurma'])
        instance.turma = turma
        instance.save()
        return instance