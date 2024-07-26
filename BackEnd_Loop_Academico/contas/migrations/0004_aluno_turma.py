# Generated by Django 5.0.6 on 2024-07-26 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0003_alter_perfil_turma'),
        ('turma', '0003_remove_turma_alunos'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='turma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='turma.turma'),
        ),
    ]
