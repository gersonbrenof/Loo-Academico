from django.db import models
from contas.models import User




class ListaExercicio(models.Model):
    DIFFICULTY_CHOICES = [
        ('Fácil e Média', 'Fácil e Média'),
        ('Médio e Difícil', 'Médio e Difícil'),
      
    ]
    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Indisponível', 'Indisponível'),
    ]
    titulo = models.CharField(max_length=100, blank=False, null=False)
    numeroExercicio = models.PositiveIntegerField(unique=True)
    dataCriacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='Disponível')
    dificuldade = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, default='Fácil e Média')
    toltaExcercicios = models.PositiveBigIntegerField(default=0, editable=False)

    def atualizar_total_exercicios(self):
        self.toltaExcercicios = self.exercicios.count()
        self.save() 
    def verificar_respostas(self):
        exercicios = self.exercicios.all()
        total_exercicios = exercicios.count()
        exercicios_respondidos = exercicios.filter(status='Respondido').count()
    
        if total_exercicios == 0:
            self.status = 'Disponível'  # Disponível se não houver exercícios
        elif exercicios_respondidos == total_exercicios:
            self.status = 'Indisponível'  # Indisponível se todos os exercícios foram respondidos
        else:
            self.status = 'Disponível'  # Disponível se nem todos os exercícios foram respondidos
        
        self.save()
    def __str__(self):
       return self.titulo
   
class Exercicio(models.Model):
    STATUS_CHOICES = [
        ('Não Respondido', 'Não Respondido'),
        ('Respondido', 'Respondido'),
    ]
    titulo = models.CharField(max_length=300)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='Não Respondido')
    numeroDoExercicio = models.PositiveIntegerField()
    entradaExemplo = models.TextField(default="", null=True, blank=True)  
    saidaExemplo = models.TextField(default="")
    lista = models.ForeignKey(ListaExercicio, related_name='exercicios', on_delete=models.CASCADE, default="100")
    def __str__(self) -> str:
        return self.titulo


class ResponderExercicio(models.Model):
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    aluno = models.ForeignKey('contas.Aluno', on_delete=models.CASCADE)
    codigoDoExercicio = models.TextField()
    resultado = models.TextField(blank=True)
    pontuacao = models.PositiveIntegerField(blank=True, null=True)
    dataEnvio = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.resultado
    

class Sintaxe(models.Model):
    titulo = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField()
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.titulo

class Problema(models.Model):
    numeroDica = models.PositiveIntegerField()
    conteudoDica = models.TextField()
    imagemExemplo = models.ImageField(upload_to='imagemProblema/', blank=True, null=True)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE,  default=1)

    def __str__(self) -> str:
        return f"Dica {self.numeroDica}"

class DiscricaoDetalhada(models.Model):
    descricao = models.TextField()
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, default=1)

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
