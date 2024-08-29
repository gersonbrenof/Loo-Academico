from rest_framework import serializers
from materialApoio.models import VideoYoutube, ArquivoPdf, MaterialApoio, MapaMental


class MapaMentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapaMental
        fields = ['id', 'mapaMental']

class VideoYoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoYoutube
        fields = ['id', 'link_youtube']

class ArquivoPdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArquivoPdf
        fields = ['id', 'arquivo']

class MaterialApoioSerializer(serializers.ModelSerializer):
    videos_youtube = VideoYoutubeSerializer(many=True, read_only=True)
    arquivos_pdf = ArquivoPdfSerializer(many=True, read_only=True)
    mapa_mental = MapaMentalSerializer(many = True, read_only=True)

    class Meta:
        model = MaterialApoio
        fields = ['id', 'titulo', 'descricao', 'quantidade_conteudo', 'videos_youtube', 'arquivos_pdf', 'mapa_mental']
    def update(self, instance, validated_data):
        # Atualizar o material de apoio com os dados fornecidos
        instance = super().update(instance, validated_data)
        # Calcular a quantidade de conteúdo
        instance.calcular_quantidade_conteudo()
        return instance