# Generated by Django 5.0.6 on 2024-06-25 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercicio', '0002_compilador_resultado_execucao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compilador',
            old_name='codico',
            new_name='codigo',
        ),
        migrations.RemoveField(
            model_name='compilador',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='compilador',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='compilador',
            name='resultado_execucao',
        ),
        migrations.RemoveField(
            model_name='compilador',
            name='updated_at',
        ),
    ]
