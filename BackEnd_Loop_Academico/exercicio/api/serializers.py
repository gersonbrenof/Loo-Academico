# compilador/api/serializers.py
from rest_framework import serializers
from exercicio.models import Compilador

class CompiladorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compilador
        fields = ['id', 'codigo_c', 'entradas', 'resultado_execucao']
