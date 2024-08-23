from django.apps import AppConfig


class ExercicioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exercicio'
    def ready(self):
          import exercicio.signals