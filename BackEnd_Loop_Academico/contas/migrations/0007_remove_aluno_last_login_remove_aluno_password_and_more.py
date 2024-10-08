# Generated by Django 5.0.6 on 2024-08-01 19:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0006_aluno_is_active_aluno_is_staff'),
        ('turma', '0004_alter_turma_codicoturma'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='aluno',
            name='password',
        ),
        migrations.AddField(
            model_name='aluno',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='turma',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='turma.turma'),
        ),
    ]
