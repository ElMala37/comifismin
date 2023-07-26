# Generated by Django 4.2.1 on 2023-05-27 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0010_alter_vente_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vente',
            name='produits',
        ),
        migrations.AddField(
            model_name='vente',
            name='client_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='AppCotisants.cotisants'),
        ),
        migrations.AddField(
            model_name='vente',
            name='prix',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vente',
            name='produit',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='vente',
            name='produit_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='AppCotisants.produits'),
        ),
        migrations.AlterField(
            model_name='vente',
            name='client',
            field=models.CharField(max_length=50),
        ),
    ]
