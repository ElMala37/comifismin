# Generated by Django 4.2.1 on 2023-06-03 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0031_alter_produits_type_produit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produits',
            name='type_produit',
            field=models.CharField(choices=[('Boisson', 'Boisson'), ('Barre de céreales/sucreries', 'Barre de céreales/sucreries'), ('Viennoiserie', 'Viennoiserie')], max_length=50),
        ),
    ]
