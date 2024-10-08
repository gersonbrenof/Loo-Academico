# Generated by Django 5.0.6 on 2024-09-19 00:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0009_aluno_exercicio_respondido'),
        ('emblemas', '0003_alter_emblema_aluno'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmblemaAluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('desbloqueado', 'Desbloqueado'), ('nao_desbloqueado', 'Não Desbloqueado')], default='nao_desbloqueado', max_length=20)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contas.aluno')),
                ('emblema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emblemas.emblema')),
            ],
            options={
                'unique_together': {('aluno', 'emblema')},
            },
        ),
    ]
