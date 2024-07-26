from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from turma.models import Turma
from django.core.validators import RegexValidator

class AlunoManager(BaseUserManager):
    def create_user(self, nomeAluno, email, matricula, institucao, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo Email deve ser preenchido')
        email = self.normalize_email(email)
        user = self.model(nomeAluno=nomeAluno, email=email, matricula=matricula, institucao=institucao, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nomeAluno, email, matricula, institucao, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário deve ter is_superuser=True.')

        return self.create_user(nomeAluno, email, matricula, institucao, password, **extra_fields)

class Aluno(AbstractBaseUser):
    nomeAluno = models.CharField(max_length=100)
    institucao = models.CharField(max_length=100)
    matricula = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex='^\d+$', message='A matrícula deve conter apenas números.')])
    email = models.EmailField(unique=True)
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True)

    objects = AlunoManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nomeAluno', 'institucao', 'matricula']


    def save(self, *args, **kwargs):
        # valida se a turma existe antes de salva
        if self.turma and not Turma.objects.filter(id=self.turma.id).exists():
            raise ValueError('Turma inválida.')
        super().save(*args, **kwargs)
    def __str__(self):
        return self.email
class Perfil(models.Model):
    fotoPerfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.aluno.nomeAluno} - {self.aluno.matricula} - {self.turma.codicoTurma}'
    