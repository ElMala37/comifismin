# Generated by Django 4.2.1 on 2023-05-28 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0025_alter_favoristibbar_produit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoristipause',
            name='produit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='favoris_tipause', to='AppCotisants.produits'),
        ),
    ]
