# Generated by Django 3.2.25 on 2024-07-20 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicodiario',
            name='folga_nao_util',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='servicodiario',
            name='folga_util',
            field=models.IntegerField(default=0),
        ),
    ]
