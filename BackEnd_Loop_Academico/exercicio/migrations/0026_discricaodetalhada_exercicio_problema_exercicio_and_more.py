# Generated by Django 5.0.6 on 2024-08-20 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercicio', '0025_alter_listaexercicio_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='discricaodetalhada',
            name='exercicio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exercicio.exercicio'),
        ),
        migrations.AddField(
            model_name='problema',
            name='exercicio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exercicio.exercicio'),
        ),
        migrations.AddField(
            model_name='sintaxe',
            name='exercicio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exercicio.exercicio'),
        ),
    ]
