from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from materialApoio.models import VideoYoutube, ArquivoPdf
from materialApoio.api.serializers import VideoYoutubeSerializer, ArquivoPdfSerializer, MaterialApoio, MaterialApoioSerializer, VisualizacaoMaterial
from materialApoio.api.serializers import MapaMental, MapaMentalSerializer
from django.db.models import Q
class MaterialApoioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MaterialApoio.objects.all()
    serializer_class = MaterialApoioSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        material = self.get_object()
        usuario = request.user

        # Cria a visualização apenas se o usuário ainda não tiver visto
        VisualizacaoMaterial.objects.get_or_create(usuario=usuario, material=material)

        serializer = self.get_serializer(material, context={'request': request})
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
    """
    Busca por Material de Apoio pelo título.
    Retorna apenas materiais cujo título contém a query.
    """
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('titulo', '').strip()

        if query:
            materiais = MaterialApoio.objects.filter(titulo__icontains=query)
        else:
            materiais = MaterialApoio.objects.none()  # Retorna vazio se não houver query

        if not materiais.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = MaterialApoioSerializer(materiais, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class MaterialApoioAdvancedSearchView(APIView):
    """
    Busca por Material de Apoio incluindo títulos de Mapas Mentais, PDFs e Vídeos do YouTube.
    Filtra cada conteúdo pelo título da query.
    """
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('titulo', '').strip()

        if not query:
            return Response([], status=status.HTTP_200_OK)

        materiais = MaterialApoio.objects.filter(
            Q(titulo__icontains=query) |
            Q(mapas_mentais__titulo__icontains=query) |
            Q(arquivos_pdf__titulo__icontains=query) |
            Q(videos_youtube__titulo__icontains=query)
        ).distinct()

        resultado = []
        for mat in materiais:
            videos = mat.videos_youtube.filter(titulo__icontains=query)
            pdfs = mat.arquivos_pdf.filter(titulo__icontains=query)
            mapas = mat.mapas_mentais.filter(titulo__icontains=query)

            if videos.exists() or pdfs.exists() or mapas.exists() or query.lower() in mat.titulo.lower():
                resultado.append({
                    "id": mat.id,
                    "titulo": mat.titulo,
                    "descricao": mat.descricao,
                    "quantidade_conteudo": mat.quantidade_conteudo,
                    "videos_youtube": [{"id": v.id, "link_youtube": v.link_youtube, "titulo": v.titulo, "descricao": v.descricao} for v in videos],
                    "arquivos_pdf": [{"id": p.id, "arquivo": p.arquivo.url, "titulo": p.titulo, "descricao": p.descricao} for p in pdfs],
                    "mapas_mentais": [{"id": m.id, "mapa_mental": m.mapa_mental.url, "titulo": m.titulo, "descricao": m.descricao} for m in mapas],
                    "visualizacoes": mat.visualizacoes,
                })

        return Response(resultado, status=status.HTTP_200_OK)