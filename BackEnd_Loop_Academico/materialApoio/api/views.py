from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Q
from materialApoio.models import VideoYoutube, ArquivoPdf, MaterialApoio, VisualizacaoMaterial
from materialApoio.api.serializers import (
    VideoYoutubeSerializer,
    ArquivoPdfSerializer,
    MaterialApoioSerializer,
    MapaMentalSerializer,
    MapaMental
)

# ----------------------------
# ViewSets padrão
# ----------------------------
class MaterialApoioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MaterialApoio.objects.all()
    serializer_class = MaterialApoioSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        material = self.get_object()
        usuario = request.user

        # Verifica se o usuário tem perfil de Aluno
        if not hasattr(usuario, 'aluno'):
            return Response({"error": "Usuário não possui perfil de aluno."}, status=400)

        aluno = usuario.aluno

        # Cria a visualização apenas se ainda não existir
        VisualizacaoMaterial.objects.get_or_create(usuario=aluno, material=material)

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

# ----------------------------
# Buscas
# ----------------------------
class MaterialApoioSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        usuario = request.user  # <-- User, não Aluno
        query = request.query_params.get('titulo', '').strip()

        if not query:
            return Response([], status=status.HTTP_200_OK)

        materiais = MaterialApoio.objects.filter(titulo__icontains=query)
        if not materiais.exists():
            return Response([], status=status.HTTP_200_OK)

        # Cria visualizações
        for mat in materiais:
            VisualizacaoMaterial.objects.get_or_create(usuario=usuario, material=mat)

        serializer = MaterialApoioSerializer(materiais, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MaterialApoioAdvancedSearchView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Busca por Material de Apoio incluindo títulos de Mapas Mentais, PDFs e Vídeos do YouTube.
    Filtra cada conteúdo pelo título da query.
    """
    def get(self, request, *args, **kwargs):
        usuario = request.user  # <-- User
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
                # Corrigido: passa o User e não o Aluno
                VisualizacaoMaterial.objects.get_or_create(usuario=usuario, material=mat)
                resultado.append({
                    "id": mat.id,
                    "titulo": mat.titulo,
                    "descricao": mat.descricao,
                    "quantidade_conteudo": mat.quantidade_conteudo,
                    "videos_youtube": [
                        {"id": v.id, "link_youtube": v.link_youtube, "titulo": v.titulo, "descricao": v.descricao} 
                        for v in videos
                    ],
                    "arquivos_pdf": [
                        {"id": p.id, "arquivo": p.arquivo.url, "titulo": p.titulo, "descricao": p.descricao} 
                        for p in pdfs
                    ],
                    "mapas_mentais": [
                        {"id": m.id, "mapa_mental": m.mapa_mental.url, "titulo": m.titulo, "descricao": m.descricao} 
                        for m in mapas
                    ],
                    "visualizacoes": mat.visualizacoes,
                })

        return Response(resultado, status=status.HTTP_200_OK)