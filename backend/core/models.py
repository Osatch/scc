from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Gantt(models.Model):
    secteur = models.IntegerField()
    nom_intervenant = models.CharField(max_length=255)
    type_intervention = models.CharField(max_length=50, choices=[('OK SAV', 'OK SAV'), ('OK RACC', 'OK RACC'), ('NOK RACC', 'NOK RACC'), ('NOK SAV', 'NOK SAV')], null=True, blank=True)
    heure_08 = models.BooleanField(default=False)
    heure_09 = models.BooleanField(default=False)
    heure_10 = models.BooleanField(default=False)
    heure_11 = models.BooleanField(default=False)
    heure_13 = models.BooleanField(default=False)
    heure_14 = models.BooleanField(default=False)
    heure_18 = models.BooleanField(default=False)
    taux_transfo = models.CharField(max_length=10)
    taux_remplissage = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nom_intervenant} - {self.type_intervention}"


class StatistiquesGantt(models.Model):
    type_intervention = models.CharField(max_length=50, choices=[('RACC', 'RACC'), ('SAV', 'SAV')])
    taux_transfo = models.CharField(max_length=10)
    nbr_inter_ok = models.IntegerField()
    nbr_inter_nok = models.IntegerField()
    nbr_inter_cours = models.IntegerField()
    nbr_inter_peril = models.IntegerField()
    nbr_inter_restant = models.IntegerField()
    pdc_jour = models.IntegerField()
    total = models.IntegerField()
    taux_remplissage = models.CharField(max_length=10)
    taux_avancement = models.CharField(max_length=10)
    attention_controle = models.IntegerField(default=0)

    def __str__(self):
        return f"Stats {self.type_intervention} - {self.taux_transfo}"


