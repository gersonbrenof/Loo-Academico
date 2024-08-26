from django.db import models


class MaterialApoio(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class VideoYoutube(models.Model):
    material_apoio = models.ForeignKey(MaterialApoio, on_delete=models.CASCADE, related_name='videos_youtube')
    link_youtube = models.URLField()

    def __str__(self):
        return self.link_youtube
    

class ArquivoPdf(models.Model):
    material_apoio = models.ForeignKey(MaterialApoio, on_delete=models.CASCADE, related_name='arquivos_pdf')
    arquivo = models.FileField(upload_to='pdfs/')
    mapaMental = models.ImageField(upload_to='mapas_mentais/', null=True, blank=True)
    def __str__(self):
        return str(self.arquivo)