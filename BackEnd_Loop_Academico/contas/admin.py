from django.contrib import admin
from .models import Aluno, Perfil
# Register your models here.
admin.site.register(Perfil)
class AlunoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Só cria o perfil se for um novo aluno
            Perfil.objects.create(aluno=obj)

admin.site.register(Aluno, AlunoAdmin)
