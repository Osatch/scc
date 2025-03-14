# Generated by Django 5.1.6 on 2025-03-15 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_relancejj_grdv_relancejj_jeton_id_field_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relancejj',
            name='grdv',
        ),
        migrations.RemoveField(
            model_name='relancejj',
            name='jeton_id_field',
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='activite',
            field=models.CharField(choices=[('SAV', 'SAV'), ('RACC', 'RACC')], max_length=4),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='commentaire_cloture',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='commentaire_demarrage',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='date_intervention',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='departement',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='heure_debut',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='heure_fin',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='heure_prevue',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='jeton',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relances', to='core.ard2'),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='numero',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='pec',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='statut',
            field=models.CharField(choices=[('Cloturée', 'Cloturée'), ('Taguée', 'Taguée'), ('Relance démarrage', 'Relance démarrage'), ('Relance Cloture', 'Relance Cloture')], max_length=20),
        ),
        migrations.AlterField(
            model_name='relancejj',
            name='techniciens',
            field=models.CharField(max_length=255),
        ),
    ]
