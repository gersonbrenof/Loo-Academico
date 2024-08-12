# Generated by Django 5.0.6 on 2024-08-12 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0008_alter_aluno_user'),
        ('forum', '0005_alter_forum_aluno'),
    ]

    operations = [
        migrations.AddField(
            model_name='respondertopico',
            name='aluno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contas.aluno'),
        ),
    ]
