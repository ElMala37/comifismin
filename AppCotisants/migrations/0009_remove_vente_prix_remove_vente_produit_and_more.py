# Generated by Django 4.2.1 on 2023-05-27 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0008_delete_panier_alter_vente_compte_serveur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vente',
            name='prix',
        ),
        migrations.RemoveField(
            model_name='vente',
            name='produit',
        ),
        migrations.AddField(
            model_name='vente',
            name='produits',
            field=models.ManyToManyField(to='AppCotisants.produits'),
        ),
    ]