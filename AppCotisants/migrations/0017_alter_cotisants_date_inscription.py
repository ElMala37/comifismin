# Generated by Django 4.2.1 on 2023-05-28 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0016_alter_cotisants_t_cotisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotisants',
            name='date_inscription',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
