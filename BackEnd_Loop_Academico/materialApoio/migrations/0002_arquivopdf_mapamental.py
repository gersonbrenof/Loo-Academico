# Generated by Django 5.0.6 on 2024-08-26 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materialApoio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='arquivopdf',
            name='mapaMental',
            field=models.ImageField(blank=True, null=True, upload_to='mapas_mentais/'),
        ),
    ]
