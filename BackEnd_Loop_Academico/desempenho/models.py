from django.db import models
from contas.models import Aluno
from turma.models import Turma
from exercicio.models import Exercicio, ResponderExercicio

class Desempenho(models.Model):
    STATUS_CHOICES = [
        ('Não Responido e Não enviado', 'Não Responido e Não enviado'),
        ('Resolução Correta', 'Resolução Correta'),
        ('Resolução Incorreta', 'Resolução Incorreta'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    pontuacaoAluno = models.PositiveIntegerField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    tentativas = models.IntegerField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Não Responido e Não enviado')
    observacao = models.CharField(max_length=500, blank=True, null=True)
    avaliacao = models.CharField(max_length=100, blank=True, null=True)
    
    total_respostas = models.IntegerField(default=0)  # Total de respostas dadas
    respostas_corretas = models.IntegerField(default=0)  # Total de respostas corretas
    
    def __str__(self):
        return f"Desempenho do aluno {self.aluno} na turma {self.turma}"
    
    @property
    def porcentagem_desempenho(self):
        if self.total_respostas == 0:
            return 0
        return (self.respostas_corretas / self.total_respostas) * 100
    
    @property
    def status_avaliacao(self):
        if self.total_respostas == 0:
            return 'Não Responido e Não enviado'
        if self.respostas_corretas == self.total_respostas:
            return 'Resolução Correta'
        return 'Resolução Incorreta'
    