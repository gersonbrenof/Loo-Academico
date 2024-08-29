from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from materialApoio.models import VideoYoutube, ArquivoPdf
from materialApoio.api.serializers import VideoYoutubeSerializer, ArquivoPdfSerializer, MaterialApoio, MaterialApoioSerializer
from materialApoio.api.serializers import MapaMental, MapaMentalSerializer
class MaterialApoioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MaterialApoio.objects.all()
    serializer_class = MaterialApoioSerializer

    def retrieve(self, request, *args, **kwargs):
        # Obtém o objeto material de apoio usando o método original
        material_apoio = self.get_object()

        # Calcula e atualiza a quantidade de conteúdo
        material_apoio.calcular_quantidade_conteudo()

        # Serializa o objeto atualizado
        serializer = self.get_serializer(material_apoio)

        # Retorna a resposta com os dados atualizados
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        # Obtém a lista de materiais de apoio
        queryset = self.get_queryset()

        # Calcula e atualiza a quantidade de conteúdo para cada material de apoio
        for material_apoio in queryset:
            material_apoio.calcular_quantidade_conteudo()
            material_apoio.save()  # Garante que a quantidade de conteúdo seja salva

        # Serializa a lista de materiais de apoio atualizados
        serializer = self.get_serializer(queryset, many=True)

        # Retorna a resposta com os dados atualizados
        return Response(serializer.data)

class VideoYoutubeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VideoYoutube.objects.all()
    serializer_class = VideoYoutubeSerializer

class MapaMentalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MapaMental.objects.all()
    serializer_class = MapaMentalSerializer

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
    