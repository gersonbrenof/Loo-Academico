from rest_framework import serializers
from emblemas.models import Emblema

class EmblemaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nomeAluno', read_only= True)
    class Meta:
        model = Emblema
        fields = ['id', 'tituloEmblema','subtiluloEmblema', 'descricao', 'imagemEmblema', 'criterio', 'aluno_nome']