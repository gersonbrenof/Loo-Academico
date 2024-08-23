from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from exercicio.models import Exercicio, ListaExercicio # Importe os modelos necessários

@receiver(post_save, sender=Exercicio)
def atualizar_total_exercicios_apos_save(sender, instance, **kwargs):
    instance.lista.atualizar_total_exercicios()

@receiver(post_delete, sender=Exercicio)
def atualizar_total_exercicios_apos_delete(sender, instance, **kwargs):
    instance.lista.atualizar_total_exercicios()