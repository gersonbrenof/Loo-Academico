# Generated by Django 5.0.6 on 2024-08-13 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercicio', '0009_alter_responderexercicio_pontuacao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listaexercicio',
            name='saidaEsperada',
            field=models.TextField(default=''),
        ),
    ]