from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.



class Gantt(models.Model):
    INTERVENTION_CHOICES = [
        ('OK SAV', 'OK SAV'),
        ('OK RACC', 'OK RACC'),
        ('NOK SAV', 'NOK SAV'),
        ('NOK RACC', 'NOK RACC'),
        ('En cours SAV', 'En cours SAV'),
        ('En cours RACC', 'En cours RACC'),
        ('Alerte SAV', 'Alerte SAV'),
        ('Alerte RACC', 'Alerte RACC'),
        ('Planifiée SAV', 'Planifiée SAV'),
        ('Planifiée RACC', 'Planifiée RACC'),
    ]

    secteur = models.IntegerField()
    nom_intervenant = models.CharField(max_length=255)
    type_intervention = models.CharField(
        max_length=50,
        choices=INTERVENTION_CHOICES,
        null=True,
        blank=True
    )
    heure_08 = models.CharField(
        max_length=50,
        choices=INTERVENTION_CHOICES,
        null=True,
        blank=True
    )
    heure_09 = models.CharField(
        max_length=50,
        choices=INTERVENTION_CHOICES,
        null=True,
        blank=True
    )
    heure_10 = models.CharField(
        max_length=50,
        choices=INTERVENTION_CHOICES,
        null=True,
        blank=True
    )
    heure_11 = models.CharField(
        max_length=50,
        choices=INTERVENTION_CHOICES,
        null=True,
        blank=True
    )
    heure_13 = models.CharField(
        max_length=50,
        choices=INTERVENTION_CHOICES,
        null=True,
        blank=True
    )
    heure_14 = models.CharField(
        max_length=50,
        choices=INTERVENTION_CHOICES,
        null=True,
        blank=True
    )
    heure_18 = models.CharField(
        max_length=50,
        choices=INTERVENTION_CHOICES,
        null=True,
        blank=True
    )
    taux_transfo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    taux_remplissage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )

    def __str__(self):
        return f"{self.nom_intervenant} - {self.type_intervention}"
#gantstat


class GanttStatistics(models.Model):
    TYPE_CHOICES = [
        ('RACC', 'RACC'),
        ('SAV', 'SAV'),
    ]

    # Champs du modèle
    type_intervention = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="Type d'intervention"
    )
    taux_transfo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Taux de transformation"
    )
    nbr_inter_cloturee_ok = models.IntegerField(
        verbose_name="Nombre d'interventions clôturées OK"
    )
    nbr_inter_cloturee_nok = models.IntegerField(
        verbose_name="Nombre d'interventions clôturées NOK"
    )
    nbr_inter_en_cours = models.IntegerField(
        verbose_name="Nombre d'interventions en cours"
    )
    nbr_inter_en_peril = models.IntegerField(
        verbose_name="Nombre d'interventions en péril"
    )
    nbr_inter_restant = models.IntegerField(
        verbose_name="Nombre d'interventions restantes"
    )
    pdc_du_jour = models.IntegerField(
        verbose_name="PDC du jour"
    )
    total = models.IntegerField(
        verbose_name="Total"
    )
    taux_remplissage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Taux de remplissage"
    )
    taux_avancement = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Taux d'avancement"
    )
    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )

    def __str__(self):
        return f"{self.type_intervention} - {self.date_mise_a_jour}"




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


#model param 
    
class Parametres(models.Model):
    # Choix pour les champs avec des options prédéfinies
    COMPETENCE_CHOICES = [
        ('SAV', 'SAV'),
        ('', 'Vide'),  # Option vide
    ]

    CONTROLE_PHOTO_CHOICES = [
        ('G1', 'G1'),
        ('G2', 'G2'),
    ]

    GRILLE_ACTIF_CHOICES = [
        ('OUI', 'OUI'),
        ('NON', 'NON'),
    ]

    ZONE_CHOICES = [
        ('Zone 1', 'Zone 1'),
        ('Zone 2', 'Zone 2'),
        # Ajoutez d'autres zones si nécessaire
    ]

    # Champs du modèle
    id_tech = models.CharField(max_length=50, unique=True, verbose_name="ID Technicien")  # Identifiant unique du technicien
    nom_tech = models.CharField(max_length=255, verbose_name="Nom du Technicien")  # Nom complet du technicien
    departement = models.CharField(max_length=255, verbose_name="Département")  # Département du technicien
    log_free = models.CharField(max_length=255, verbose_name="Log Free")  # Format : tsm_prenom_nom
    competence = models.CharField(max_length=3, choices=COMPETENCE_CHOICES, blank=True, verbose_name="Compétence")  # Compétence SAV ou vide
    actif_depuis = models.DateField(verbose_name="Actif depuis")  # Date depuis laquelle le technicien est actif
    controle_photo = models.CharField(max_length=2, choices=CONTROLE_PHOTO_CHOICES, verbose_name="Contrôle Photo")  # G1 ou G2
    manager = models.CharField(max_length=255, verbose_name="Manager")  # Nom du manager (ex: Rayane Balere)
    zone = models.CharField(max_length=50, choices=ZONE_CHOICES, verbose_name="Zone")  # Zone 1, Zone 2, etc.
    grille_actif = models.CharField(max_length=3, choices=GRILLE_ACTIF_CHOICES, verbose_name="Grille Actif")  # OUI ou NON
    log_technicien = models.CharField(max_length=255, verbose_name="Log Technicien")  # Log du technicien
    mdp = models.CharField(max_length=255, verbose_name="Mot de passe")  # Mot de passe

    def __str__(self):
        return f"{self.id_tech} - {self.nom_tech}"

    class Meta:
        verbose_name = "Paramètre"
        verbose_name_plural = "Paramètres"



#le nok from django.db import models

class NOK(models.Model):
    jeton = models.CharField(max_length=20)
    date_rdv = models.DateField()
    type_intervention = models.CharField(max_length=50, choices=[
        ('Pose de PTO ZMD', 'Pose de PTO ZMD'),
        ('Pose de PTO ZTD', 'Pose de PTO ZTD'),
        ('SAV', 'SAV'),
        ('PON', 'PON'),
        ('Remise en conformité', 'Remise en conformité'),
        ('null', 'Null'),
    ])
    question = models.CharField(max_length=50, choices=[
        ('Appel CA ?', 'Appel CA ?'),
        ('Null', 'Null'),
    ])
    reponse = models.CharField(max_length=50, choices=[
        ('Non', 'Non'),
        ('Pas d’appel CA effectué', 'Pas d’appel CA effectué'),
        ('CA injoignable', 'CA injoignable'),
        ('Null', 'Null'),
    ])
    reponse_libre = models.CharField(max_length=255, blank=True, null=True)
    tech_nom_prenom = models.CharField(max_length=100)
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.jeton} - {self.date_rdv}"