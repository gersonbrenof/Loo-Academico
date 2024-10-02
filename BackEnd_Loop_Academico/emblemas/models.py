from django.db import models
from contas.models import Aluno

from django.db import models


class Emblema(models.Model):
    STATUS_CHOICES = [
        ('desbloqueado', 'Desbloqueado'),
        ('nao_desbloqueado', 'Não Desbloqueado'),
    ]

    tituloEmblema = models.CharField(max_length=100)
    subtituloEmblema = models.CharField(max_length=250, default="")
    codigoEmblema = models.CharField(max_length=10, unique=True)
    imagemEmblema = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    criterio = models.CharField(max_length=255)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='emblemas', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_desbloqueado')

    def __str__(self):
        return self.tituloEmblema
    

class EmblemaAluno(models.Model):
    STATUS_CHOICES = [
        ('desbloqueado', 'Desbloqueado'),
        ('nao_desbloqueado', 'Não Desbloqueado'),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    emblema = models.ForeignKey(Emblema, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_desbloqueado')

    class Meta:
        unique_together = ('aluno', 'emblema')  # Garante que um aluno tenha um único registro para cada emblema

    def __str__(self):
        return f"{self.aluno.nomeAluno} - {self.emblema.tituloEmblema} ({self.status})"