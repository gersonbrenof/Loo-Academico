from rest_framework import serializers
from emblemas.models import Emblema, EmblemaAluno
from contas.models import Aluno
class EmblemaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.SerializerMethodField()

    class Meta:
        model = Emblema
        fields = ['id', 'tituloEmblema', 'subtituloEmblema', 'codigoEmblema', 'imagemEmblema', 'criterio', 'aluno_nome', 'status']

    def get_aluno_nome(self, obj):
        # Retorna o nome do aluno associado, ou None se não houver aluno
        if obj.aluno:
            return obj.aluno.nomeAluno
        return None
    
from emblemas.models import Emblema, EmblemaAluno
from rest_framework import serializers

class EmblemaAlunoSerializer(serializers.ModelSerializer):
    tituloEmblema = serializers.CharField(source='emblema.tituloEmblema')
    subtituloEmblema = serializers.CharField(source='emblema.subtituloEmblema')
    codigoEmblema = serializers.CharField(source='emblema.codigoEmblema')
    imagemEmblema = serializers.ImageField(source='emblema.imagemEmblema')
    criterio = serializers.CharField(source='emblema.criterio')

    class Meta:
        model = EmblemaAluno
        fields = ['id', 'tituloEmblema', 'subtituloEmblema', 'codigoEmblema', 'imagemEmblema', 'criterio', 'status']
class EmblemaListaTudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emblema
        fields = ['id', 'tituloEmblema','subtituloEmblema', 'codigoEmblema', 'imagemEmblema', 'criterio', 'status']