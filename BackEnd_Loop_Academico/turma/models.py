from django.db import models

class Turma(models.Model):
    codicoTurma = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self):
        return self.codicoTurma