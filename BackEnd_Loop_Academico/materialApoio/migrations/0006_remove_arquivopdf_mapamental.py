# Generated by Django 5.0.6 on 2024-08-29 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materialApoio', '0005_materialapoio_quantidade_conteudo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arquivopdf',
            name='mapaMental',
        ),
    ]
