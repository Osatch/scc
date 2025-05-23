# Generated by Django 5.1.6 on 2025-04-19 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_gantt_commentaire_08_gantt_commentaire_09_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debriefracc',
            name='appel_tech',
            field=models.CharField(blank=True, choices=[("Pas d'appel", "Pas d'appel"), ('Appel à chaud', 'Appel à chaud'), ('Appel après clôture', 'Appel après clôture')], max_length=20, null=True, verbose_name='Appel tech'),
        ),
        migrations.AlterField(
            model_name='debriefracc',
            name='resultat_controle',
            field=models.CharField(blank=True, choices=[('RAS', 'RAS'), ('Ecart detecte', 'Ecart detecte')], max_length=100, null=True, verbose_name='Résultat du contrôle'),
        ),
    ]
