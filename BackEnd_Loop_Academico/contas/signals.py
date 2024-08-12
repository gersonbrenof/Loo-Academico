# contas/signals.py
import logging

logger = logging.getLogger(__name__)
logger.info('signals.py loaded')

from django.db.models.signals import post_save
from django.dispatch import receiver
from contas.models import Aluno, Perfil

@receiver(post_save, sender=Aluno)
def create_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(aluno=instance)
        logger.info(f'Perfil criado para o aluno {instance.email}')
