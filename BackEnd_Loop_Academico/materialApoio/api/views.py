from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from materialApoio.models import VideoYoutube, ArquivoPdf
from materialApoio.api.serializers import VideoYoutubeSerializer, ArquivoPdfSerializer

class VideoYoutubeViewSet(viewsets.ModelViewSet):
    queryset = VideoYoutube.objects.all()
    serializer_class = VideoYoutubeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [ 'get']

class ArquivosPdfViewSet(viewsets.ModelViewSet):
    queryset = ArquivoPdf.objects.all()
    serializer_class = ArquivoPdfSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [ 'get']