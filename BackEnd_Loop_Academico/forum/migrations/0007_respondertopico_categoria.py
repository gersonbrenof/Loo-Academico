# Generated by Django 5.0.6 on 2024-08-21 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercicio', '0026_discricaodetalhada_exercicio_problema_exercicio_and_more'),
        ('forum', '0006_respondertopico_aluno'),
    ]

    operations = [
        migrations.AddField(
            model_name='respondertopico',
            name='categoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exercicio.listaexercicio'),
        ),
    ]