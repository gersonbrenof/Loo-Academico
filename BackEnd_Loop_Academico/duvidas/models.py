from django.db import models
from contas.models import Aluno
class Duvidas(models.Model):
    titulo = models.CharField(max_length=250, null=False, blank=False)
    duvidaAluno = models.TextField()
    data_criacao = models.DateField(auto_now_add=True)
    status_resposta = models.BooleanField(default=False)
    tematica = models.CharField(max_length=200) # adcionar um forey quei da lista de tarefa modifcar depois
    aluno = models.ForeignKey( Aluno, on_delete=models.CASCADE, null=True, blank=True)
    anonimo = models.BooleanField(default=True)
    def salva_duvida(self, usuario, anonimo = True):
        if anonimo:
            self.aluno = None
            self.anonimo = True
        else:
            self.aluno = usuario
            self.anonimo = False
        self.save()

    def __str__(self):
        return self.titulo
    


