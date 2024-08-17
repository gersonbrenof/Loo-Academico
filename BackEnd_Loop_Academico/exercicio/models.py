from django.db import models
from contas.models import Aluno
class Exercicio(models.Model):
    STATUS_CHOICES = [
        ('N', 'Não Respondido'),
        ('R', 'Respondido'),
    ]
    titulo = models.CharField(max_length=300)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    numeroDoExercicio = models.PositiveIntegerField()
    entradaExemplo = models.TextField(default="", null=True, blank=True)  
    saidaExemplo = models.TextField(default="")
    def __str__(self) -> str:
        return self.titulo

class ListaExercicio(models.Model):
    DIFFICULTY_CHOICES = [
        ('F', 'Fácil'),
        ('M', 'Médio'),
        ('D', 'Difícil'),
    ]
    titulo = models.CharField(max_length=100, blank=False, null=False)
    numeroExercicio = models.PositiveIntegerField(unique=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    dificuldade = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES, default='F')
    totalExercicio = models.ManyToManyField(Exercicio)

    def __str__(self):
        return self.titulo

class ResponderExercicio(models.Model):
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    codigoDoExercicio = models.TextField()
    resultado = models.TextField(blank=True)
    pontuacao = models.PositiveIntegerField(blank=True, null=True)
    dataEnvio = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.codigoDoExercicio
    

class Sintaxe(models.Model):
    titulo = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField()

    def __str__(self):
        return self.titulo

class Problema(models.Model):
    numeroDica = models.PositiveIntegerField()
    conteudoDica = models.TextField()
    imagemExemplo = models.ImageField(upload_to='imagemProblema/', blank=True, null=True)

    def __str__(self) -> str:
        return f"Dica {self.numeroDica}"

class DiscricaoDetalhada(models.Model):
    descricao = models.TextField()

    def __str__(self):
        return self.descricao[:50]  # Exibe os primeiros 50 caracteres da descrição

class DicaAluno(models.Model):
    codigoApoio = models.TextField()
    descricaoDetalhada = models.ForeignKey(DiscricaoDetalhada, on_delete=models.CASCADE)
    sintaxe = models.ForeignKey(Sintaxe, on_delete=models.CASCADE)
    problema = models.ForeignKey(Problema, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codigoApoio} - {self.exercicio.titulo}"
