from django.db import models
from contas.models import Aluno

class Forum(models.Model):
    titulo = models.CharField(max_length=300, blank=False, null=False)
    descricao = models.TextField(blank=True, null=True)
    data_inico = models.DateTimeField(auto_now_add=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.titulo

class ResponderTopico(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    respostaForum = models.TextField()
    data_resposta = models.DateTimeField(auto_now_add=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null =True, blank=True)

    def __str__(self):
        return f"Resposta ao topico: {self.forum.titulo}"
    