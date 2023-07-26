# Generated by Django 4.2.1 on 2023-05-28 19:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCotisants', '0015_alter_cotisants_t_cotisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotisants',
            name='t_cotisation',
            field=models.DurationField(choices=[(datetime.timedelta(days=365), '1 an'), (datetime.timedelta(days=183), '6 mois'), (datetime.timedelta(days=6), '6 jours')], default=None),
        ),
    ]
