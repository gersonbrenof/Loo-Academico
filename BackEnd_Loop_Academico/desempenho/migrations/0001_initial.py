# Generated by Django 5.0.6 on 2024-08-22 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contas', '0009_aluno_exercicio_respondido'),
        ('turma', '0004_alter_turma_codicoturma'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desempenho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pontuacaoAluno', models.PositiveIntegerField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('tentativas', models.IntegerField()),
                ('tempo_resolucao', models.DurationField()),
                ('status', models.CharField(choices=[('Não Responido e Não enviado', 'Não Responido e Não enviado'), ('Resolução Correta', 'Resolução Correta'), ('Resolução Incorreta', 'Resolução Incorreta')], default='Não Responido e Não enviado', max_length=30)),
                ('observacao', models.CharField(blank=True, max_length=500, null=True)),
                ('avaliacao', models.CharField(blank=True, max_length=100, null=True)),
                ('total_respostas', models.IntegerField(default=0)),
                ('respostas_corretas', models.IntegerField(default=0)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contas.aluno')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turma.turma')),
            ],
        ),
    ]
