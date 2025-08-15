from rest_framework import serializers
from materialApoio.models import VideoYoutube, ArquivoPdf, MaterialApoio, MapaMental


class MapaMentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapaMental
        fields = ['id', 'mapa_mental','titulo','descricao']

class VideoYoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoYoutube
        fields = ['id', 'link_youtube','titulo','descricao']

class ArquivoPdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArquivoPdf
        fields = ['id', 'arquivo','titulo','descricao']

class MaterialApoioSerializer(serializers.ModelSerializer):
    videos_youtube = VideoYoutubeSerializer(many=True, read_only=True)
    arquivos_pdf = ArquivoPdfSerializer(many=True, read_only=True)
    mapas_mentais = MapaMentalSerializer(many=True, read_only=True)  # <-- corrigido

    class Meta:
        model = MaterialApoio
        fields = [
            'id', 'titulo', 'descricao', 'quantidade_conteudo',
            'videos_youtube', 'arquivos_pdf', 'mapas_mentais', 'visualizacoes'
        ]
    def update(self, instance, validated_data):
        # Atualizar o material de apoio com os dados fornecidos
        instance = super().update(instance, validated_data)
        # Calcular a quantidade de conteúdo
        instance.calcular_quantidade_conteudo()
        return instance