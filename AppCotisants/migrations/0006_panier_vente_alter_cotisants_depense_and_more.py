# Generated by Django 4.2.1 on 2023-05-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0005_cotisants_nomprenom'),
    ]

    operations = [
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produit_nom', models.CharField(max_length=30, unique=True)),
                ('produit_prix', models.FloatField()),
                ('produit_Id', models.IntegerField()),
                ('client_nom', models.CharField(max_length=30, unique=True)),
                ('client_Id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=30)),
                ('compte_serveur', models.CharField(max_length=30)),
                ('produit', models.CharField(max_length=30)),
                ('prix', models.FloatField(default=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='cotisants',
            name='depense',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='cotisants',
            name='solde',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='produits',
            name='prix',
            field=models.FloatField(default=1),
        ),
    ]
