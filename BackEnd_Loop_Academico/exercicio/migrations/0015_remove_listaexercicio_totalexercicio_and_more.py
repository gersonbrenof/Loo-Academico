# Generated by Django 5.0.6 on 2024-08-17 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercicio', '0014_remove_listaexercicio_totalexercicio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listaexercicio',
            name='totalExercicio',
        ),
        migrations.AlterField(
            model_name='listaexercicio',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
