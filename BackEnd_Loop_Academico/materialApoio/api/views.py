from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from materialApoio.models import VideoYoutube, ArquivoPdf
from materialApoio.api.serializers import VideoYoutubeSerializer, ArquivoPdfSerializer, MaterialApoio, MaterialApoioSerializer
class MaterialApoioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MaterialApoio.objects.all()
    serializer_class = MaterialApoioSerializer

class VideoYoutubeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VideoYoutube.objects.all()
    serializer_class = VideoYoutubeSerializer

class ArquivoPdfViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArquivoPdf.objects.all()
    serializer_class = ArquivoPdfSerializer

class MaterialApoioSearchView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtém o parâmetro de busca do request
        query = request.query_params.get('titulo', '').strip()
        
        # Realiza a busca por materiais cujo título contém a query
        if query:
            materiais = MaterialApoio.objects.filter(titulo__icontains=query)
        else:
            materiais = MaterialApoio.objects.all()
        
        # Serializa os dados encontrados
        serializer = MaterialApoioSerializer(materiais, many=True)
        
        # Se nenhum material for encontrado, retorna uma lista vazia
        if not materiais:
            return Response([], status=status.HTTP_200_OK)
        
        # Retorna os dados serializados como resposta
        return Response(serializer.data, status=status.HTTP_200_OK)