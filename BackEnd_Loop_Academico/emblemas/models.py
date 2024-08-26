from django.db import models
from contas.models import Aluno

from django.db import models

class Emblema(models.Model):
    STATUS_CHOICES = [
        ('desbloqueado', 'Desbloqueado'),
        ('nao_desbloqueado', 'Não Desbloqueado'),
    ]
    
    tituloEmblema = models.CharField(max_length=100, null=False, blank=False)
    subtituloEmblema = models.CharField(max_length=250, null=False, blank=False, default="")
    codigoEmblema = models.CharField(max_length=10, unique=True, null=False, blank=False)
    imagemEmblema = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    criterio = models.CharField(max_length=255, blank=False, null=False)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='emblema', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_desbloqueado')

    def __str__(self):
        return self.tituloEmblema
