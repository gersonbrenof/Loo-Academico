# compilador/models.py
from django.db import models

class Compilador(models.Model):
    codigo_c = models.TextField()
    entradas = models.TextField(default='')  # Entradas opcionais para o programa C
    resultado_execucao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Compilador ID: {self.id}"
