# Generated by Django 4.2.1 on 2023-05-27 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0006_panier_vente_alter_cotisants_depense_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='panier',
            name='client_Id',
        ),
        migrations.RemoveField(
            model_name='panier',
            name='client_nom',
        ),
    ]
