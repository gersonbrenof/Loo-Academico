from django.db import models
from django.contrib.auth.models import User

class MaterialApoio(models.Model):
    titulo = models.CharField(max_length=150,blank=False, null=False, default='Sem título')
    descricao = models.TextField(blank=True, null=True)
    quantidade_conteudo = models.IntegerField(default=0)
    visualizacoes = models.PositiveIntegerField(default=0)
    

    def calcular_quantidade_conteudo(self):
        total_videos = self.videos_youtube.count()
        total_pdfs = self.arquivos_pdf.count()
        total_mapas_mentais = self.mapas_mentais.count()

        self.quantidade_conteudo = total_videos + total_pdfs + total_mapas_mentais
        self.save()

    def __str__(self):
        return self.titulo

class VisualizacaoMaterial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey('MaterialApoio', on_delete=models.CASCADE, related_name='visualizacoes_usuario')
    data_visualizacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'material')  # Garante 1 visualização por usuário por material
class VideoYoutube(models.Model):
    material_apoio = models.ForeignKey(MaterialApoio, on_delete=models.CASCADE, related_name='videos_youtube')
    titulo = models.CharField(max_length=150,blank=False, null=False, default='Sem título')
    descricao = models.TextField(blank=True, null=True)
    link_youtube = models.URLField()

    def __str__(self):
        return self.titulo


class ArquivoPdf(models.Model):
    material_apoio = models.ForeignKey(MaterialApoio, on_delete=models.CASCADE, related_name='arquivos_pdf')
    titulo = models.CharField(max_length=150,blank=False, null=False, default='Sem título')
    descricao = models.TextField(blank=True, null=True)
    arquivo = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.titulo


class MapaMental(models.Model):
    material_apoio = models.ForeignKey(MaterialApoio, on_delete=models.CASCADE, related_name='mapas_mentais')
    titulo = models.CharField(max_length=150,blank=False, null=False, default='Sem título')
    descricao = models.TextField(blank=True, null=True)
    mapa_mental = models.ImageField(upload_to='mapas_mentais/', null=True, blank=True)

    def __str__(self):
        return self.titulo
    