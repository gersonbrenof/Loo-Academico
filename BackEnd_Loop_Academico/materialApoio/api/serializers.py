from rest_framework import serializers
from materialApoio.models import VideoYoutube, ArquivoPdf, MaterialApoio
class VideoYoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoYoutube
        fields = ['id', 'link_youtube']

class ArquivoPdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArquivoPdf
        fields = ['id', 'arquivo', 'mapaMental']

class MaterialApoioSerializer(serializers.ModelSerializer):
    videos_youtube = VideoYoutubeSerializer(many=True, read_only=True)
    arquivos_pdf = ArquivoPdfSerializer(many=True, read_only=True)

    class Meta:
        model = MaterialApoio
        fields = ['id', 'titulo', 'descricao', 'videos_youtube', 'arquivos_pdf']