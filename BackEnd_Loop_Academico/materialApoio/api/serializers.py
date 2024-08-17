from rest_framework import serializers
from materialApoio.models import VideoYoutube, ArquivoPdf

class VideoYoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoYoutube
        fields = ['id','titulo','link_youtube']

class ArquivoPdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArquivoPdf
        fields = ['id','titulo','arquivo']
