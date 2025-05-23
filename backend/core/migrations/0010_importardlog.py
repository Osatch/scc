# Generated by Django 5.1.6 on 2025-04-16 10:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_ard2_date_rendez_vous'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportARDLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier_nom', models.CharField(max_length=255)),
                ('import_date', models.DateTimeField(auto_now_add=True)),
                ('duree', models.FloatField(help_text='Durée en secondes')),
                ('resultat', models.TextField(help_text='Log brut du traitement')),
                ('utilisateur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
