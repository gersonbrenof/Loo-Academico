# Generated by Django 5.0.6 on 2024-08-14 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercicio', '0012_exercicio_saidaexemplo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercicio',
            name='entradaExemplo',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
