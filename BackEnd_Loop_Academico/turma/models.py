from django.db import models
from django.contrib.auth.models import User
class Turma(models.Model):
    codicoTurma = models.CharField(max_length=10, unique=True, default="12345")
    
    def __str__(self):
        return self.codicoTurma