from django.db import models

class MaterialApoio(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField( blank=True, null=True)

    def __str__(self):
        return self.titulo
    

class VideoYoutube(MaterialApoio):
    link_youtube = models.URLField()

    def __str__(self):
        return self.link_youtube
    
class ArquivoPdf(MaterialApoio):
    arquivo = models.FileField(upload_to='pdfs/')

    
