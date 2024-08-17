from django.db import models
from contas.models import Aluno

class Emblema(models.Model):
    tituloEmblema= models.CharField(max_length=100 , null=False, blank=False)
    subtiluloEmblema = models.CharField(max_length=250, null=False, blank=False, default="")
    descricao = models.TextField()
    imagemEmblema = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    criterio = models.CharField(max_length=255, blank=False, null=False)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='emblema', null=True, blank=True)

    def __str__(self):
        return self.tituloEmblema
