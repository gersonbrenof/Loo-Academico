# Generated by Django 5.0.6 on 2024-08-20 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0008_alter_aluno_user'),
        ('exercicio', '0026_discricaodetalhada_exercicio_problema_exercicio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='exercicio_respondido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='exercicio.exercicio'),
        ),
    ]