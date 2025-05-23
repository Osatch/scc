# Generated by Django 5.1.6 on 2025-04-03 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_debriefsav_societe'),
    ]

    operations = [
        migrations.AddField(
            model_name='debriefsav',
            name='appel_tech',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Statut Appel Tech'),
        ),
        migrations.AddField(
            model_name='debriefsav',
            name='manager',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Manager'),
        ),
        migrations.AddField(
            model_name='debriefsav',
            name='resultat_controle',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Résultat Contrôle'),
        ),
        migrations.AlterField(
            model_name='debriefsav',
            name='synchro',
            field=models.CharField(blank=True, choices=[('Echec', 'Echec'), ('Taguée', 'Taguée'), ('OK', 'OK')], max_length=10, null=True, verbose_name='Synchro'),
        ),
    ]
