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
    heure_12 = models.CharField(
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
    heure_15 = models.CharField(
        max_length=50,
        choices=INTERVENTION_CHOICES,
        null=True,
        blank=True
    )
    heure_16 = models.CharField(
        max_length=50,
        choices=INTERVENTION_CHOICES,
        null=True,
        blank=True
    )
    heure_17 = models.CharField(
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
    
from django.db import models

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



#Control photo 

from django.db import models
from .models import RelanceJJ  # Assurez-vous d'importer le modèle RelanceJJ

class ControlPhoto(models.Model):
    GROUPE_TECH_CHOICES = [
        ('G1', 'G1'),
        ('G2', 'G2'),
        # Ajoutez d'autres groupes si nécessaire
    ]

    ZONE_MANAGER_CHOICES = [
        ('Zone1', 'Zone1'),
        ('Zone2', 'Zone2'),
        ('#N/A', '#N/A'),
    ]

    STATUT_CHOICES = [
        ('Taguée', 'Taguée'),
        ('Cloturée', 'Cloturée'),
    ]

    STATUT_PTO_CHOICES = [
        ('//', '//'),
        ('PTO et CAB absents', 'PTO et CAB absents'),
        ('première pose nécessaire', 'première pose nécessaire'),
    ]

    SYNCHRO_CHOICES = [
        ('OK', 'OK'),
        ('NOK', 'NOK'),
    ]

    RESULTATS_VERIFICATION_CHOICES = [
        ('Rectifié et validé', 'Rectifié et validé'),
        ('Non validé', 'Non validé'),
    ]

    jeton = models.ForeignKey(RelanceJJ, on_delete=models.CASCADE, related_name='control_photos')  # Référence au jeton de la table RelanceJJ
    date = models.DateField()  # Date d'intervention de RelanceJJ
    heure = models.TimeField()  # Heure d'intervention de RelanceJJ
    tech = models.CharField(max_length=255)  # Nom du technicien de RelanceJJ
    groupe_tech = models.CharField(max_length=2, choices=GROUPE_TECH_CHOICES)  # Groupe tech (G1, G2, ...)
    actif_depuis = models.DateField()  # Date du début d'activité de l'agent
    zone_manager = models.CharField(max_length=10, choices=ZONE_MANAGER_CHOICES, null=True, blank=True)  # Zone/Manager (Zone1, Zone2, #N/A)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)  # Statut de RelanceJJ
    secteur = models.CharField(max_length=255)  # Secteur de RelanceJJ
    statut_pto = models.CharField(max_length=50, choices=STATUT_PTO_CHOICES, null=True, blank=True)  # Statut PTO
    synchro = models.CharField(max_length=3, choices=SYNCHRO_CHOICES, null=True, blank=True)  # Synchro (OK, NOK)
    agent = models.CharField(max_length=255)  # Nom de l'agent qui a suivi le technicien (PEC PAR de RelanceJJ)
    resultats_verification = models.CharField(max_length=50, choices=RESULTATS_VERIFICATION_CHOICES, null=True, blank=True)  # Résultats vérification
    commentaire = models.TextField(null=True, blank=True)  # Commentaire

    def __str__(self):
        return f"{self.jeton.jeton} - {self.date} - {self.tech}"

    def save(self, *args, **kwargs):
        # Vous pouvez ajouter ici des logiques supplémentaires si nécessaire
        super().save(*args, **kwargs)



#control a froid
from django.db import models
from .models import ControlPhoto  # Assurez-vous d'importer le modèle ControlPhoto

class Controlafroid(models.Model):
    # Relation avec le modèle ControlPhoto
    control_photo = models.OneToOneField(ControlPhoto, on_delete=models.CASCADE, related_name='controlafroid')

    # Champs supplémentaires
    RESULTAT_AFROID_CHOICES = [
        ('Validé', 'Validé'),
        ('Non validé', 'Non validé'),
        ('null', 'null'),
    ]

    COMMENTAIRE_CHOICES = [
        ('PTO prise zoomer + decharge pto dans le placard / rectifié et validé', 
         'PTO prise zoomer + decharge pto dans le placard / rectifié et validé'),
        ('photo Mur avant travaux entamer / photo Mur après ne montre pas le PTO / REF PTO éronnée', 
         'photo Mur avant travaux entamer / photo Mur après ne montre pas le PTO / REF PTO éronnée'),
        ('null', 'null'),
    ]

    resultat_a_froid = models.CharField(
        max_length=20,
        choices=RESULTAT_AFROID_CHOICES,
        default='null',
        verbose_name='Résultat à froid'
    )

    commentaire = models.CharField(
        max_length=150,  # Longueur suffisante pour stocker les commentaires
        choices=COMMENTAIRE_CHOICES,
        default='null',
        verbose_name='Commentaire'
    )

    class Meta:
        verbose_name = 'Control à froid'
        verbose_name_plural = 'Controls à froid'

    def __str__(self):
        return f"Control à froid pour {self.control_photo.Jeton}"



#debrief racc 

from django.db import models
from .models import RelanceJJ, Parametres, ARD2

class DebriefRACC(models.Model):
    # Choix pour les champs avec des options prédéfinies
    APPEL_TECH_CHOICES = [
        ("Pas d'appel", "Pas d'appel"),
        ("Appel à chaud", "Appel à chaud"),
        ('null', 'null'),
    ]

    SYNCHRO_CHOICES = [
        ('Echec', 'Echec'),
        ('Taguées', 'Taguées'),
        ('null', 'null'),
    ]

    TYPE_ECHEC_CHOICES = [
        ('Echec client', 'Echec client'),
        ('Echec d\'acces', 'Echec d\'acces'),
        ('null', 'null'),
    ]

    RESULTAT_CONTROLE_CHOICES = [
        ('RAS', 'RAS'),
        ('null', 'null'),
    ]

    # Champs du modèle
    jeton = models.ForeignKey(RelanceJJ, on_delete=models.CASCADE, related_name='debrief_racc', limit_choices_to={'activite': 'RACC'})  # Référence au jeton de la table RelanceJJ (uniquement pour les activités RACC)
    date = models.DateField()  # Date d'intervention de RelanceJJ
    heure = models.TimeField()  # Heure d'intervention de RelanceJJ
    tech = models.CharField(max_length=255)  # Nom du technicien de RelanceJJ
    numero_technicien = models.CharField(max_length=50)  # Numéro de RelanceJJ
    nouveaux_tech = models.DateField()  # Date qui vient de Parametres (actif_depuis)
    zone_manager = models.CharField(max_length=255)  # Vient de manager de Parametres
    code_cloture_technicien = models.TextField()  # Texte libre
    reference_pm = models.CharField(max_length=50)  # Vient avec le numéro de jeton de ARD2
    appel_tech = models.CharField(max_length=20, choices=APPEL_TECH_CHOICES, default='null')  # Appel tech
    synchro = models.CharField(max_length=20, choices=SYNCHRO_CHOICES, default='null')  # Synchro
    secteur = models.CharField(max_length=255)  # Secteur de RelanceJJ
    type_echec = models.CharField(max_length=20, choices=TYPE_ECHEC_CHOICES, default='null')  # Type d'échec
    pec_par = models.CharField(max_length=255)  # PEC PAR de RelanceJJ
    resultat_controle = models.CharField(max_length=10, choices=RESULTAT_CONTROLE_CHOICES, default='null')  # Résultat du contrôle
    diagnostic = models.TextField()  # Texte libre pour le diagnostic

    def __str__(self):
        return f"{self.jeton.jeton} - {self.date} - {self.tech}"

    def save(self, *args, **kwargs):
        # Remplir automatiquement les champs à partir de RelanceJJ, Parametres et ARD2
        if not self.date:
            self.date = self.jeton.date_intervention
        if not self.heure:
            self.heure = self.jeton.heure_prevue
        if not self.tech:
            self.tech = self.jeton.techniciens
        if not self.numero_technicien:
            self.numero_technicien = self.jeton.numero
        if not self.pec_par:
            self.pec_par = self.jeton.pec

        # Récupérer les informations de Parametres
        try:
            param = Parametres.objects.get(id_tech=self.jeton.techniciens)
            self.nouveaux_tech = param.actif_depuis
            self.zone_manager = param.manager
        except Parametres.DoesNotExist:
            pass

        # Récupérer les informations de ARD2
        try:
            ard2 = ARD2.objects.get(jeton_commande=self.jeton.jeton.jeton_commande)
            self.reference_pm = ard2.pm
        except ARD2.DoesNotExist:
            pass

        super().save(*args, **kwargs)

#debrief SAV

from django.db import models
from .models import RelanceJJ, Parametres, ARD2

class DebriefSAV(models.Model):
    # Choix pour les champs avec des options prédéfinies
    APPEL_TECH_CHOICES = [
        ("Pas d'appel", "Pas d'appel"),
        ("Appel à chaud", "Appel à chaud"),
        (None, 'null'),
    ]

    SYNCHRO_CHOICES = [
        ('Echec', 'Echec'),
        ('Taguée', 'Taguée'),
        (None, 'null'),
    ]

    TYPE_ECHEC_CHOICES = [
        ('Echec client', 'Echec client'),
        ('Echec d\'acces', 'Echec d\'acces'),
        (None, 'null'),
    ]

    RESULTAT_CONTROLE_CHOICES = [
        ('RAS', 'RAS'),
        (None, 'null'),
    ]

    # Champs du modèle
    jeton = models.ForeignKey(RelanceJJ, on_delete=models.CASCADE, related_name='debriefs_sav', limit_choices_to={'activite': 'SAV'})
    date = models.DateField(verbose_name="Date d'intervention")  # Date d'intervention de RelanceJJ
    heure = models.TimeField(verbose_name="Heure d'intervention")  # Heure d'intervention de RelanceJJ
    tech = models.CharField(max_length=255, verbose_name="Nom du technicien")  # Nom du technicien de RelanceJJ
    numero_tech = models.CharField(max_length=50, verbose_name="Numéro du technicien")  # Numéro de RelanceJJ
    nouveaux_tech = models.DateField(verbose_name="Nouveaux tech", null=True, blank=True)  # Date qui vient de Parametres
    zone_manager = models.CharField(max_length=255, verbose_name="Zone/Manager", null=True, blank=True)  # Vient de manager de Parametres
    code_cloture_tech = models.TextField(verbose_name="Code clôture technicien", null=True, blank=True)  # Texte libre
    reference_pm = models.CharField(max_length=50, verbose_name="Référence PM", null=True, blank=True)  # Vient avec le numéro de jeton de ARD2
    appel_tech = models.CharField(max_length=20, choices=APPEL_TECH_CHOICES, verbose_name="Appel tech", null=True, blank=True)  # Choix prédéfinis
    synchro = models.CharField(max_length=10, choices=SYNCHRO_CHOICES, verbose_name="Synchro", null=True, blank=True)  # Choix prédéfinis
    secteur = models.CharField(max_length=255, verbose_name="Secteur", null=True, blank=True)  # Secteur de RelanceJJ
    type_echec = models.CharField(max_length=20, choices=TYPE_ECHEC_CHOICES, verbose_name="Type d'échec", null=True, blank=True)  # Choix prédéfinis
    pec_par = models.CharField(max_length=255, verbose_name="PEC par", null=True, blank=True)  # PEC PAR de RelanceJJ
    resultat_controle = models.CharField(max_length=10, choices=RESULTAT_CONTROLE_CHOICES, verbose_name="Résultat du contrôle", null=True, blank=True)  # Choix prédéfinis
    diagnostic = models.TextField(verbose_name="Diagnostic", null=True, blank=True)  # Texte libre

    def __str__(self):
        return f"{self.jeton.jeton} - {self.date} - {self.tech}"

    def save(self, *args, **kwargs):
        # Récupérer les données supplémentaires des modèles Parametres et ARD2
        if not self.nouveaux_tech:
            parametre = Parametres.objects.filter(id_tech=self.numero_tech).first()
            if parametre:
                self.nouveaux_tech = parametre.actif_depuis

        if not self.zone_manager:
            parametre = Parametres.objects.filter(id_tech=self.numero_tech).first()
            if parametre:
                self.zone_manager = parametre.zone

        if not self.reference_pm:
            ard2 = ARD2.objects.filter(jeton_commande=self.jeton.jeton).first()
            if ard2:
                self.reference_pm = ard2.pm

        super().save(*args, **kwargs)