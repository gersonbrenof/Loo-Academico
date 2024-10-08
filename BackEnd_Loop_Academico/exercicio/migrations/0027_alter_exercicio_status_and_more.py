# Generated by Django 5.0.6 on 2024-08-22 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercicio', '0026_discricaodetalhada_exercicio_problema_exercicio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercicio',
            name='status',
            field=models.CharField(choices=[('Não Respondido', 'Não Respondido'), ('Respondido', 'Respondido')], default='Não Respondido', max_length=14),
        ),
        migrations.AlterField(
            model_name='listaexercicio',
            name='dificuldade',
            field=models.CharField(choices=[('Fácil e Média', 'Fácil e Média'), ('Médio e Difícil', 'Médio e Difícil')], default='Fácil e Média', max_length=30),
        ),
        migrations.AlterField(
            model_name='listaexercicio',
            name='status',
            field=models.CharField(choices=[('Disponível', 'Disponível'), ('Indisponível', 'Indisponível')], default='Disponível', max_length=14),
        ),
    ]
