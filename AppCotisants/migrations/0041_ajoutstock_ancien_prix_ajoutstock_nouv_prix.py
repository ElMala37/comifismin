# Generated by Django 4.2.1 on 2023-06-04 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0040_alter_cotisants_depense_alter_cotisants_nomprenom_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ajoutstock',
            name='ancien_prix',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=8),
        ),
        migrations.AddField(
            model_name='ajoutstock',
            name='nouv_prix',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=8),
        ),
    ]
