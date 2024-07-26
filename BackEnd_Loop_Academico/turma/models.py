from django.db import models
from django.contrib.auth.models import User
class Turma(models.Model):
    codicoTurma = models.CharField(max_length=10, null=True, blank=True)
    
    def __str__(self):
        return self.codicoTurma