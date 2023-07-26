# Generated by Django 4.2.1 on 2023-05-28 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0020_rename_date_connexion_supvente_date_suppression'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotisants',
            name='depense',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='encaissement',
            name='montant',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='produits',
            name='prix',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='supvente',
            name='prix',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='vente',
            name='prix',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
