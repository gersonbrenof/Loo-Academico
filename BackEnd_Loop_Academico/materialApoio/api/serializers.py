from rest_framework import serializers
from materialApoio.models import VideoYoutube, ArquivoPdf, MaterialApoio, MapaMental, VisualizacaoMaterial


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
    mapas_mentais = MapaMentalSerializer(many=True, read_only=True)
    
    visualizado_pelo_usuario = serializers.SerializerMethodField()

    class Meta:
        model = MaterialApoio
        fields = [
            'id', 'titulo', 'descricao', 'quantidade_conteudo',
            'videos_youtube', 'arquivos_pdf', 'mapas_mentais',
            'visualizado_pelo_usuario'
        ]

    def get_visualizado_pelo_usuario(self, obj):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            return False  # request ou user não disponível
        user = request.user
        if user.is_anonymous:
            return False
        # Verifica se o usuário já visualizou o material
        return obj.visualizacoes_usuario.filter(usuario=user).exists()