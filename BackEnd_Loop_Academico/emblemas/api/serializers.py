from rest_framework import serializers
from emblemas.models import Emblema
from contas.models import Aluno
class EmblemaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nomeAluno', read_only= True)
    class Meta:
        model = Emblema
        fields = ['id', 'tituloEmblema','subtituloEmblema', 'codigoEmblema', 'imagemEmblema', 'criterio', 'aluno_nome', 'status']

class EmblemaListaTudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emblema
        fields = ['id', 'tituloEmblema','subtituloEmblema', 'codigoEmblema', 'imagemEmblema', 'criterio', 'status']