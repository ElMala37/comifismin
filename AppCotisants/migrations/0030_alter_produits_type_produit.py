# Generated by Django 4.2.1 on 2023-06-03 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0029_catproduit_modepaiement_promo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produits',
            name='type_produit',
            field=models.CharField(max_length=50),
        ),
    ]
