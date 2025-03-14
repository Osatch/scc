# Generated by Django 5.1.6 on 2025-03-13 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_interventionssav'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterventionsRACC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_jeton', models.CharField(max_length=100, unique=True)),
                ('date_intervention', models.DateField()),
                ('heure_debut', models.TimeField()),
                ('techniciens_initial', models.CharField(max_length=100)),
                ('techniciens_intervenant', models.CharField(blank=True, max_length=100, null=True)),
                ('nbr_nok', models.IntegerField(default=0)),
                ('nbr_ok', models.IntegerField(default=0)),
                ('total_interventions', models.IntegerField(default=0)),
                ('ref_pm', models.CharField(max_length=100)),
                ('dernier_echec', models.CharField(blank=True, choices=[('Client absent', 'Client absent'), ('Freebox non reçue', 'Freebox non reçue'), ('Client réalise les travaux', 'Client réalise les travaux'), ('Autorisation propriétaire', 'Autorisation propriétaire'), ('Accès refusé (Syndic/Copro)', 'Accès refusé (Syndic/Copro)'), ('Pas d accès PBO', 'Pas d accès PBO'), ('Manque de consommable', 'Manque de consommable'), ('Pas d Accès PM', 'Pas d Accès PM'), ('Autorisation du propriétaire', 'Autorisation du propriétaire'), ('RDV non honoré', 'RDV non honoré'), ('Fourreau à déboucher (intérieur)', 'Fourreau à déboucher (intérieur)'), ('Kit laissé mais non scanné', 'Kit laissé mais non scanné'), ('Refus d accès abonné', 'Refus d accès abonné')], max_length=100, null=True)),
                ('secteur', models.CharField(max_length=10)),
                ('contre_appel_client', models.TextField(blank=True, null=True)),
                ('secu', models.TextField(blank=True, null=True)),
                ('heure_demarrage', models.DateTimeField(blank=True, null=True)),
                ('heure_cloture', models.DateTimeField(blank=True, null=True)),
                ('synchro', models.CharField(blank=True, choices=[('OK', 'OK'), ('NOK', 'NOK'), ('Null', 'Null')], max_length=10, null=True)),
                ('resultat_jj', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Intervention RACC',
                'verbose_name_plural': 'Interventions RACC',
            },
        ),
    ]
