# Generated by Django 5.0.6 on 2024-09-05 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duvidas', '0002_rename_status_respsota_duvidas_status_resposta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duvidas',
            name='status_resposta',
            field=models.CharField(choices=[('AGUARDADANDO RESPOSTA', 'AGUARDADANDO RESPOSTA'), ('RESPONDIDA', 'RESPONDIDA')], default='AGUARDADANDO RESPOSTA', max_length=40),
        ),
    ]