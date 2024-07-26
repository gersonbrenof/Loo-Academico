# compilador/models.py
from django.db import models

class Exercicio(models.Model):
    STATUS_CHOICES =[
        ('N', 'Náo Respondido'),
        ('R', 'Respondido'),
    ]
    titulo = models.CharField(max_length=300)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    numeroDoExercico = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.titulo
