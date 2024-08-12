from django.contrib import admin
from exercicio.models import Exercicio, ResponderExercicio, ListaExercicio, Sintaxe, Problema, DicaAluno, DiscricaoDetalhada

admin.site.register(Exercicio)
admin.site.register(ListaExercicio)
admin.site.register(ResponderExercicio)
admin.site.register(Sintaxe)
admin.site.register(DiscricaoDetalhada)
admin.site.register(Problema)
admin.site.register(DicaAluno)

