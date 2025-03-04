from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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




#Le Model ard2 



class ARD2(models.Model):
    JETON_MAX_LENGTH = 10
    PM_MAX_LENGTH = 50

    ETAT_CHOICES = [
        ('OK', 'OK'),
        ('NOK', 'NOK'),
    ]

    jeton_commande = models.CharField(max_length=JETON_MAX_LENGTH, unique=True)
    debut_intervention = models.DateTimeField()
    fin_intervention = models.DateTimeField(null=True, blank=True)
    terminee = models.BooleanField(default=False)
    etat_intervention = models.CharField(max_length=3, choices=ETAT_CHOICES)
    technicien = models.CharField(max_length=255)
    departement = models.CharField(max_length=255)
    pm = models.CharField(max_length=PM_MAX_LENGTH)
    date_importation = models.DateTimeField(null=True, blank=True)  # Ajout sans auto_now_add

    def save(self, *args, **kwargs):
        self.terminee = bool(self.fin_intervention)
        if not self.date_importation:
            self.date_importation = timezone.now()  # Ajoute une date si vide
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.jeton_commande} - {self.technicien}"
  
  #Relance jj



class RelanceJJ(models.Model):
    ACTIVITE_CHOICES = [
        ('SAV', 'SAV'),
        ('RACC', 'RACC'),
    ]

    STATUT_CHOICES = [
        ('Cloturée', 'Cloturée'),
        ('Taguée', 'Taguée'),
        ('Relance démarrage', 'Relance démarrage'),
        ('Relance Cloture', 'Relance Cloture'),
    ]

    date_intervention = models.DateField()  # Date de l'intervention
    jeton = models.ForeignKey('ARD2', on_delete=models.CASCADE, related_name='relances')  # Référence au jeton de la table ARD2
    activite = models.CharField(max_length=4, choices=ACTIVITE_CHOICES)  # Activité (SAV ou RACC)
    heure_prevue = models.TimeField()  # Heure prévue pour l'intervention
    heure_debut = models.TimeField(null=True, blank=True)  # Heure de début de l'intervention (synchronisé avec ARD2)
    heure_fin = models.TimeField(null=True, blank=True)  # Heure de fin de l'intervention (synchronisé avec ARD2)
    techniciens = models.CharField(max_length=255)  # Nom des techniciens
    numero = models.CharField(max_length=50)  # Numéro
    departement = models.CharField(max_length=255)  # Département de ARD2
    pec = models.CharField(max_length=255)  # Agents qui ont suivi l'intervention
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)  # Statut de l'intervention
    commentaire_demarrage = models.TextField(null=True, blank=True)  # Commentaire démarrage
    commentaire_cloture = models.TextField(null=True, blank=True)  # Commentaire clôture

    def save(self, *args, **kwargs):
        # Synchroniser heure_debut et heure_fin avec ARD2
        if self.jeton.debut_intervention:
            self.heure_debut = self.jeton.debut_intervention.time()  # Extrait l'heure de début
        if self.jeton.fin_intervention:
            self.heure_fin = self.jeton.fin_intervention.time()  # Extrait l'heure de fin

        # Logique pour déterminer le statut
        if self.heure_debut and self.heure_fin:
            self.statut = 'Cloturée'
        elif self.heure_debut and not self.heure_fin:
            self.statut = 'Taguée'
        elif not self.heure_debut and timezone.now().time() > self.heure_prevue:
            self.statut = 'Relance démarrage'
        elif self.heure_fin and self.heure_fin == timezone.datetime.min.time():
            self.statut = 'Relance Cloture'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.jeton.jeton_commande} - {self.date_intervention} - {self.activite}"