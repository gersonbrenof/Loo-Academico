from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from turma.models import Turma
from django.core.validators import RegexValidator

from django.contrib.auth.models import User

def create_user_with_email(email, password):
    user = User.objects.create_user(
        username=email,  # Usa o email como o username
        email=email,
        password=password
    )
    return user
class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    nomeAluno = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=100)
    matricula = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex='^\d+$', message='A matrícula deve conter apenas números.')]
    )
    email = models.EmailField(unique=True)
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Necessário para permissões e acesso ao admin


    def save(self, *args, **kwargs) :
        self.user.username = self.email
        self.user.email = self.email
        self.user.save()
        super(Aluno,self).save(*args, **kwargs)

    def __str__(self):
        return self.email
class Perfil(models.Model):
    fotoPerfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        # Verifica se 'turma' não é None antes de acessar 'codicoTurma'
        turma_codigo = self.turma.codicoTurma if self.turma else 'Sem turma'
        return f'{self.aluno.nomeAluno} - {turma_codigo}'
    