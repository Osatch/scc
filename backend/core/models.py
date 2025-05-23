#AbstractUserfrom django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.

# Create your models here.

# Les rôles multi utilisateurs ***************************
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models



# Définition des rôles disponibles pour vos utilisateurs
ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('chef_plateau', 'Chef de plateau'),
    ('manager', 'Manager'),
    ('agent', 'Agent'),
    ('technicien', 'Technicien'),
    ('direction', 'Direction'),
    ('user', 'Utilisateur'),
]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role='user', **extra_fields):
        """
        Crée et enregistre un utilisateur avec l'email et le mot de passe donnés.
        Le rôle par défaut est 'user'.
        """
        if not email:
            raise ValueError("L'email doit être renseigné")
        # Normaliser l'email pour éviter les duplications
        email = self.normalize_email(email)
        # Créer l'instance de l'utilisateur avec le rôle et les autres champs supplémentaires
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Crée et enregistre un superutilisateur avec l'email et le mot de passe donnés.
        Pour un superutilisateur, le rôle est forcé à 'admin' et certains flags sont définis.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role='admin', **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=191)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    # Champ pour définir le rôle de l'utilisateur
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email





#le GRDV *****************************************

from django.db import models

class GRDV(models.Model):
    # Ajout du champ jeton
    jeton = models.CharField(max_length=255, verbose_name="Jeton", blank=True, default="")

    date_rdv = models.DateTimeField(verbose_name="Date et heure du rendez-vous")
    debut = models.DateTimeField(verbose_name="Date et heure du début d'intervention")
    fin = models.DateTimeField(verbose_name="Date et heure de fin d'intervention")
    statut_rendez_vous = models.CharField(max_length=255, verbose_name="Statut du rendez-vous")
    statut_grdv = models.CharField(max_length=255, verbose_name="Statut GRDV")
    activite = models.CharField(max_length=255, verbose_name="Activité")
    plp = models.CharField(max_length=255, verbose_name="PLP")
    technicien = models.CharField(max_length=255, verbose_name="Technicien")
    presta = models.CharField(max_length=255, verbose_name="Presta")
    tel_contact = models.CharField(max_length=20, verbose_name="Téléphone de contact")
    commentaire = models.TextField(verbose_name="Commentaire")
    adresse_postale = models.CharField(max_length=255, verbose_name="Adresse postale")
    ref_commande = models.CharField(max_length=255, verbose_name="Référence de commande")
    nro = models.CharField(max_length=255, verbose_name="NRO")
    pm = models.CharField(max_length=255, verbose_name="PM")
    code = models.CharField(max_length=255, verbose_name="Code")
    residence = models.CharField(max_length=255, verbose_name="Résidence")
    bat = models.CharField(max_length=255, verbose_name="Bâtiment")
    esc = models.CharField(max_length=255, verbose_name="Escalier")
    eta = models.CharField(max_length=255, verbose_name="Étage")
    por = models.CharField(max_length=255, verbose_name="Porte")
    pto = models.CharField(max_length=255, verbose_name="PTO")
    id_client = models.CharField(max_length=255, verbose_name="ID Client")
    technologement = models.CharField(max_length=255, verbose_name="Technologement")
    operateurlogement = models.CharField(max_length=255, verbose_name="Opérateur logement")
    typezone = models.CharField(max_length=255, verbose_name="Type de zone")
    typetechno = models.CharField(max_length=255, verbose_name="Type de technologie")
    secteur_infra = models.CharField(max_length=255, verbose_name="Secteur infrastructure")
    typebatiment = models.CharField(max_length=255, verbose_name="Type de bâtiment")
    typepoteau_edf = models.CharField(max_length=255, verbose_name="Type de poteau EDF")
    typeclient = models.CharField(max_length=255, verbose_name="Type de client")
    typebox = models.CharField(max_length=255, verbose_name="Type de box")
    id_debrief_rdv = models.CharField(max_length=255, verbose_name="ID Débrief RDV")
    debrief_rdv = models.TextField(verbose_name="Débrief RDV")
    Adresse_PM = models.CharField(max_length=255, verbose_name="Adresse PM")
    Connecteur_Free_PM = models.CharField(max_length=255, verbose_name="Connecteur Free PM")
    date_import = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure d'import du fichier")

    def __str__(self):
        return f"GRDV {self.id} - {self.date_rdv}"

    class Meta:
        verbose_name = "GRDV"
        verbose_name_plural = "GRDVs"

#gantt================================================================================================================
#gantt================================================================================================================
from django.db import models

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

    date_intervention = models.DateField()
    secteur = models.IntegerField()
    departement = models.CharField(max_length=255, null=True, blank=True)
    nom_intervenant = models.CharField(max_length=255)
    societe = models.CharField(max_length=255, null=True, blank=True)

    heure_08 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)
    heure_09 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)
    heure_10 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)
    heure_11 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)
    heure_12 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)
    heure_13 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)
    heure_14 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)
    heure_15 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)
    heure_16 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)
    heure_17 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)
    heure_18 = models.CharField(max_length=50, choices=INTERVENTION_CHOICES, null=True, blank=True)

    jeton_08 = models.CharField(max_length=10, blank=True, null=True)
    jeton_09 = models.CharField(max_length=10, blank=True, null=True)
    jeton_10 = models.CharField(max_length=10, blank=True, null=True)
    jeton_11 = models.CharField(max_length=10, blank=True, null=True)
    jeton_12 = models.CharField(max_length=10, blank=True, null=True)
    jeton_13 = models.CharField(max_length=10, blank=True, null=True)
    jeton_14 = models.CharField(max_length=10, blank=True, null=True)
    jeton_15 = models.CharField(max_length=10, blank=True, null=True)
    jeton_16 = models.CharField(max_length=10, blank=True, null=True)
    jeton_17 = models.CharField(max_length=10, blank=True, null=True)
    jeton_18 = models.CharField(max_length=10, blank=True, null=True)

    heure_debut_08 = models.TimeField(null=True, blank=True)
    heure_fin_08 = models.TimeField(null=True, blank=True)

    heure_debut_09 = models.TimeField(null=True, blank=True)
    heure_fin_09 = models.TimeField(null=True, blank=True)

    heure_debut_10 = models.TimeField(null=True, blank=True)
    heure_fin_10 = models.TimeField(null=True, blank=True)

    heure_debut_11 = models.TimeField(null=True, blank=True)
    heure_fin_11 = models.TimeField(null=True, blank=True)

    heure_debut_12 = models.TimeField(null=True, blank=True)
    heure_fin_12 = models.TimeField(null=True, blank=True)

    heure_debut_13 = models.TimeField(null=True, blank=True)
    heure_fin_13 = models.TimeField(null=True, blank=True)

    heure_debut_14 = models.TimeField(null=True, blank=True)
    heure_fin_14 = models.TimeField(null=True, blank=True)

    heure_debut_15 = models.TimeField(null=True, blank=True)
    heure_fin_15 = models.TimeField(null=True, blank=True)

    heure_debut_16 = models.TimeField(null=True, blank=True)
    heure_fin_16 = models.TimeField(null=True, blank=True)

    heure_debut_17 = models.TimeField(null=True, blank=True)
    heure_fin_17 = models.TimeField(null=True, blank=True)

    heure_debut_18 = models.TimeField(null=True, blank=True)
    heure_fin_18 = models.TimeField(null=True, blank=True)

    motif_retard_08 = models.TextField(blank=True, null=True)
    commentaire_08 = models.TextField(blank=True, null=True)

    motif_retard_09 = models.TextField(blank=True, null=True)
    commentaire_09 = models.TextField(blank=True, null=True)

    motif_retard_10 = models.TextField(blank=True, null=True)
    commentaire_10 = models.TextField(blank=True, null=True)

    motif_retard_11 = models.TextField(blank=True, null=True)
    commentaire_11 = models.TextField(blank=True, null=True)

    motif_retard_12 = models.TextField(blank=True, null=True)
    commentaire_12 = models.TextField(blank=True, null=True)

    motif_retard_13 = models.TextField(blank=True, null=True)
    commentaire_13 = models.TextField(blank=True, null=True)

    motif_retard_14 = models.TextField(blank=True, null=True)
    commentaire_14 = models.TextField(blank=True, null=True)

    motif_retard_15 = models.TextField(blank=True, null=True)
    commentaire_15 = models.TextField(blank=True, null=True)

    motif_retard_16 = models.TextField(blank=True, null=True)
    commentaire_16 = models.TextField(blank=True, null=True)

    motif_retard_17 = models.TextField(blank=True, null=True)
    commentaire_17 = models.TextField(blank=True, null=True)

    motif_retard_18 = models.TextField(blank=True, null=True)
    commentaire_18 = models.TextField(blank=True, null=True)

    taux_transfo = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    taux_remplissage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom_intervenant} - {self.date_intervention}"

    def get_creneau(self, heure):
        return {
            'statut': getattr(self, f'heure_{heure}'),
            'jeton': getattr(self, f'jeton_{heure}')
        }




#gantstat===================================================================================================


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




#Le Model ard2 ===================================================================================


class ARD2(models.Model):
    JETON_MAX_LENGTH = 10
    PM_MAX_LENGTH = 50

    ETAT_CHOICES = [
        ('OK', 'OK'),
        ('NOK', 'NOK'),
    ]

    jeton_commande = models.CharField(max_length=JETON_MAX_LENGTH, unique=True)
    debut_intervention = models.DateTimeField(null=True, blank=True)
    fin_intervention = models.DateTimeField(null=True, blank=True)
    terminee = models.BooleanField(default=False)
    etat_intervention = models.CharField(max_length=3, choices=ETAT_CHOICES)
    technicien = models.CharField(max_length=255)
    departement = models.CharField(max_length=255)
    pm = models.CharField(max_length=PM_MAX_LENGTH)
    date_rendez_vous = models.DateTimeField(null=True, blank=True)  # ✅ ajout ici
    date_importation = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.terminee = bool(self.fin_intervention)
        if not self.date_importation:
            self.date_importation = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.jeton_commande} - {self.technicien}"


  

# Relance jj =====================================================================================

import unicodedata
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RelanceJJ(models.Model):
    ACTIVITE_CHOICES = [
        ('SAV', 'SAV'),
        ('RACC', 'RACC'),
    ]
    STATUT_CHOICES = [
        ('Cloturée', 'Cloturée'),
        ('Taguée', 'Taguée'),
    ]
    TYPE_STATUT_RETARD_CHOICES = [
        ('Retard démarrage', 'Retard démarrage'),
        ('Retard clôture', 'Retard clôture'),
        ('Faux démarrage', 'Faux démarrage'),
        ('Arrivé en avance', 'Arrivé en avance'),
    ]

    grdv = models.ForeignKey(
        GRDV,
        on_delete=models.CASCADE,
        related_name='relances',
        null=True,
        blank=True,
        verbose_name="GRDV associé"
    )
    date_rdv = models.DateField(null=True, blank=True, verbose_name="Date RDV (provenant de GRDV.date_rdv)")
    activite = models.CharField(max_length=4, choices=ACTIVITE_CHOICES, blank=True, verbose_name="Activité")
    heure_prevue = models.TimeField(null=True, blank=True, verbose_name="Heure prévue")
    jeton_commande = models.CharField(max_length=10, verbose_name="Jeton commande", blank=True)
    techniciens = models.CharField(max_length=255, blank=True, verbose_name="Techniciens")
    numero = models.CharField(max_length=50, verbose_name="Numéro", blank=True)
    departement = models.CharField(max_length=255, blank=True, verbose_name="Département")
    societe = models.CharField(max_length=255, blank=True, verbose_name="Société")
    pec = models.CharField(max_length=255, verbose_name="PEC", blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, blank=True, verbose_name="Statut")
    synchro = models.CharField(max_length=10, blank=True, verbose_name="Statut de synchronisation (provenant de ARD2.etat_intervention)")
    commentaire_demarrage = models.TextField(null=True, blank=True, verbose_name="Commentaire démarrage")
    commentaire_cloture = models.TextField(null=True, blank=True, verbose_name="Commentaire clôture")
    heure_debut = models.TimeField(null=True, blank=True, verbose_name="Heure début")
    heure_fin = models.TimeField(null=True, blank=True, verbose_name="Heure fin")

    # ========= Champs ajoutés pour statuer sur les retards =========
    type_statut_retard = models.CharField(
        max_length=30,
        choices=TYPE_STATUT_RETARD_CHOICES,
        blank=True,
        verbose_name="Type de Statut de Retard"
    )
    details_retard = models.TextField(
        blank=True,
        verbose_name="Détails sur le retard"
    )
    pec_retard_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Statuté par"
    )
    date_statut_retard = models.DateTimeField(
        auto_now_add=True,
        null=True,  # IMPORTANT pour éviter l'erreur de migration
        blank=True,
        verbose_name="Date de la prise de statut"
    )
    # ===============================================================

    def save(self, *args, **kwargs):
        if self.grdv:
            self.date_rdv = self.grdv.date_rdv.date() if self.grdv.date_rdv else None

            if self.grdv.activite == "RDV-Sav":
                self.activite = "SAV"
            elif self.grdv.activite == "":
                self.activite = ""
            elif self.grdv.activite == "REC-Route mise à jour via Emutation":
                self.activite = "REC"
            else:
                self.activite = "RACC"
            self.heure_prevue = self.grdv.debut.time() if self.grdv.debut else None

            if self.grdv.ref_commande:
                self.jeton_commande = unicodedata.normalize("NFKC", self.grdv.ref_commande.strip())[:10]
            else:
                self.jeton_commande = ""

        if self.heure_debut and self.heure_fin:
            self.statut = "Cloturée"
        elif self.heure_debut and not self.heure_fin:
            self.statut = "Taguée"
        else:
            self.statut = ""

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.jeton_commande} - {self.date_rdv} - {self.activite}"


#model param =======================================================================================
    


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
        ('Oui', 'Oui'),
        ('Non', 'Non'),
    ]

    ZONE_CHOICES = [
        ('Zone 1', 'Zone 1'),
        ('Zone 2', 'Zone 2'),
        # Ajoutez d'autres zones si nécessaire
    ]

    # Champs du modèle
    id_tech = models.CharField(max_length=50, unique=True, verbose_name="ID Technicien")
    nom_tech = models.CharField(max_length=255, verbose_name="Nom du Technicien")
    departement = models.CharField(max_length=255, verbose_name="Département")
    log_free = models.CharField(max_length=255, verbose_name="Log Free")
    competence = models.CharField(max_length=3, choices=COMPETENCE_CHOICES, blank=True, verbose_name="Compétence")
    actif_depuis = models.DateField(verbose_name="Actif depuis")
    controle_photo = models.CharField(max_length=2, choices=CONTROLE_PHOTO_CHOICES, verbose_name="Contrôle Photo")
    manager = models.CharField(max_length=255, verbose_name="Manager")
    zone = models.CharField(max_length=50, choices=ZONE_CHOICES, verbose_name="Zone")
    grille_actif = models.CharField(max_length=3, choices=GRILLE_ACTIF_CHOICES, verbose_name="Grille Actif")
    
    # Champs optionnels existants
    log_technicien = models.CharField(max_length=255, verbose_name="Log Technicien", blank=True, null=True)
    mdp = models.CharField(max_length=255, verbose_name="Mot de passe", blank=True, null=True)
    
    # Nouveaux champs optionnels existants
    numero_technicien = models.CharField(max_length=50, verbose_name="Numéro du Technicien", blank=True, null=True)
    societe = models.CharField(max_length=255, verbose_name="Société", blank=True, null=True)
    
    # Nouvelles colonnes ajoutées
    nom_prenom_grdv = models.CharField(max_length=255, verbose_name="Nom prénom Grdv", blank=True, null=True)
    id_grdv = models.CharField(max_length=255, verbose_name="ID Grdv", blank=True, null=True)

    def __str__(self):
        return f"{self.id_tech} - {self.nom_tech}"

    class Meta:
        verbose_name = "Paramètre"
        verbose_name_plural = "Paramètres"




#le nok =================================================================
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



#Control photo =================================================================================
from django.db import models

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
        ("Remise en conformité", "Remise en conformité"),
        ("NE", "NE"),
        ("PTO et CAB presents,conformes et exploitables", "PTO et CAB presents,conformes et exploitables"),
        ("conformes a remplacer", "conformes a remplacer"),
        ("PTO a remettre en conformité et CAB conforme", "PTO a remettre en conformité et CAB conforme"),
        ("PTO present et CAB non conforme a remplacer", "PTO present et CAB non conforme a remplacer"),
        ("PTO mal positionné a déplacer et nouveau CAB a poser", "PTO mal positionné a déplacer et nouveau CAB a poser"),
        ("PTO et CAB absent", "PTO et CAB absent"),
        ("première pose nécessaire", "première pose nécessaire"),
        ("PTO a deplacer par confort et nouveau CAB a poser", "PTO a deplacer par confort et nouveau CAB a poser"),
    ]

    SYNCHRO_CHOICES = [
        ('OK', 'OK'),
        ('NOK', 'NOK'),
    ]

    RESULTATS_VERIFICATION_CHOICES = [
        ('Validé', 'Validé'),
        ('Débrief modifié','Débrief modifié'),
        ('Non validé', 'Non validé'),
    ]

    jeton = models.CharField(max_length=255)
    date = models.DateField()
    heure = models.TimeField()
    tech = models.CharField(max_length=255)
    groupe_tech = models.CharField(max_length=2, choices=GROUPE_TECH_CHOICES)
    actif_depuis = models.DateField()
    zone_manager = models.CharField(max_length=10, choices=ZONE_MANAGER_CHOICES, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    secteur = models.CharField(max_length=255)
    statut_pto = models.CharField(max_length=100, choices=STATUT_PTO_CHOICES, null=True, blank=True)

    synchro = models.CharField(max_length=3, choices=SYNCHRO_CHOICES, null=True, blank=True)
    agent = models.CharField(max_length=255)
    resultats_verification = models.CharField(max_length=50, choices=RESULTATS_VERIFICATION_CHOICES, null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)

    societe = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    statut_appel = models.CharField(max_length=50, null=True, blank=True)

    # Champs ajoutés
    resultats_verification2 = models.CharField(max_length=50, choices=RESULTATS_VERIFICATION_CHOICES, null=True, blank=True)
    agent2 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.jeton} - {self.date} - {self.tech}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



#control a froid==================================================================================================================
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



#debrief racc =======================================================================
from django.db import models

class DebriefRACC(models.Model):
    # Champs principaux (issus d'autres modèles ou saisis)
    jeton = models.CharField(max_length=10, verbose_name="Jeton")
    date = models.DateField(null=True, blank=True, verbose_name="Date")
    tech = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tech")
    numero_technicien = models.CharField(max_length=50, null=True, blank=True, verbose_name="Numéro technicien")
    nouveaux_tech = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nouveaux tech")
    zone_manager = models.CharField(max_length=255, null=True, blank=True, verbose_name="Zone / manager")
    code_cloture_technicien = models.TextField(null=True, blank=True, verbose_name="Code clôture technicien")
    reference_pm = models.CharField(max_length=255, null=True, blank=True, verbose_name="Référence PM")

    # ✅ Nouveaux champs
    societe = models.CharField(max_length=255, null=True, blank=True, verbose_name="Société")
    manager = models.CharField(max_length=255, null=True, blank=True, verbose_name="Manager")

    # Choix prédéfinis
    APPEL_TECH_CHOICES = [
        ("Pas d'appel", "Pas d'appel"),
        ("Appel à chaud", "Appel à chaud"),
        ("Appel après clôture","Appel après clôture"),

    ]
    SYNCHRO_CHOICES = [
        ('Echec', 'Echec'),
        ('Taguées', 'Taguées'),
    ]
    TYPE_ECHEC_CHOICES = [
        ("Echec client", "Echec client"),
        ("Echec d'acces", "Echec d'acces"),
    ]
    RESULTAT_CONTROLE_CHOICES = [
        ('RAS', 'RAS'),
        ('Ecart detecte','Ecart detecte'),
    ]

    appel_tech = models.CharField(
        max_length=20,
        choices=APPEL_TECH_CHOICES,
        null=True,
        blank=True,
        verbose_name="Appel tech"
    )
    synchro = models.CharField(
        max_length=20,
        choices=SYNCHRO_CHOICES,
        null=True,
        blank=True,
        verbose_name="Synchro"
    )
    secteur = models.CharField(max_length=255, null=True, blank=True, verbose_name="Secteur")
    type_echec = models.CharField(
        max_length=50,
        choices=TYPE_ECHEC_CHOICES,
        null=True,
        blank=True,
        verbose_name="Type d'échec"
    )
    pec_par = models.CharField(max_length=255, null=True, blank=True, verbose_name="PEC par")
    resultat_controle = models.CharField(
        max_length=100,
        choices=RESULTAT_CONTROLE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Résultat du contrôle"
    )
    diagnostic = models.TextField(null=True, blank=True, verbose_name="Diagnostic")
    action = models.TextField(null=True, blank=True, verbose_name="Action")

    def __str__(self):
        return f"{self.jeton} - {self.date} - {self.tech}"




#debrief SAV ===============================================================================
from django.db import models
from .models import RelanceJJ, Parametres, ARD2

class DebriefSAV(models.Model):
    jeton = models.ForeignKey(
        RelanceJJ,
        on_delete=models.CASCADE,
        related_name='debriefs_sav',
        limit_choices_to={'activite': 'SAV'}
    )
    jeton_commande = models.CharField(
        max_length=100,
        verbose_name="Jeton Commande",
        editable=False,
        blank=True
    )
    
    societe = models.CharField(
        max_length=255,
        verbose_name="Société",
        null=True,
        blank=True
    )

    date = models.DateField(verbose_name="Date d'intervention")
    heure = models.TimeField(verbose_name="Heure d'intervention")
    tech = models.CharField(max_length=255, verbose_name="Nom du technicien")
    numero_tech = models.CharField(max_length=50, verbose_name="Numéro du technicien")
    
    tel_contact = models.CharField(
        max_length=20,
        verbose_name="Téléphone de contact",
        null=True,
        blank=True
    )
    secteur = models.CharField(
        max_length=255,
        verbose_name="Secteur",
        null=True,
        blank=True
    )
    integration = models.CharField(
        max_length=255,
        verbose_name="Intégration",
        null=True,
        blank=True
    )
    zone_manager = models.CharField(
        max_length=255,
        verbose_name="Zone / Manager",
        null=True,
        blank=True
    )
    manager = models.CharField(
        max_length=255,
        verbose_name="Manager",
        null=True,
        blank=True
    )
    termine = models.BooleanField(default=False, verbose_name="Terminé")

    synchro = models.CharField(
        max_length=10,
        choices=[
            ('Echec', 'Echec'),
            ('Taguée', 'Taguée'),
            ('OK', 'OK'),
        ],
        verbose_name="Synchro",
        null=True,
        blank=True
    )

    reference_pm = models.CharField(
        max_length=50,
        verbose_name="Référence PM",
        null=True,
        blank=True
    )

    appel_tech = models.CharField(
        max_length=255,
        verbose_name="Statut Appel Tech",
        null=True,
        blank=True
    )

    resultat_controle = models.CharField(
        max_length=50,
        verbose_name="Résultat Contrôle",
        null=True,
        blank=True
    )

    issu_intervention = models.TextField(
        verbose_name="Issu de l'intervention",
        null=True,
        blank=True
    )
    pec_par = models.CharField(
        max_length=255,
        verbose_name="PEC par",
        null=True,
        blank=True
    )
    code_cloture = models.TextField(
        verbose_name="Code clôture",
        null=True,
        blank=True
    )
    debrief = models.TextField(
        verbose_name="Débrief",
        null=True,
        blank=True
    )
    photos = models.TextField(
        verbose_name="Photos",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.jeton.jeton_commande} - {self.date} - {self.tech}"

    def save(self, *args, **kwargs):
        self.jeton_commande = self.jeton.jeton_commande

        if not self.zone_manager or not self.manager:
            parametre = Parametres.objects.filter(id_tech=self.numero_tech).first()
            if parametre:
                if not self.zone_manager:
                    self.zone_manager = parametre.zone
                if not self.manager:
                    self.manager = parametre.manager

        if not self.reference_pm:
            ard2 = ARD2.objects.filter(jeton_commande=self.jeton.jeton_commande).first()
            if ard2:
                self.reference_pm = ard2.pm

        super().save(*args, **kwargs)



#inter sav

class InterventionsSAV(models.Model):
    # Liste des choix pour le statut de l'intervention
    STATUS_CHOICES = [
        ('2906', '2906 - Freebox Etape 2/3'),
        ('3705', '3705 - Pas d\'accès au local PM'),
        ('OK', 'OK'),
        ('3510', '3510 - Tube / Fibre HS'),
        ('3204', '3204 - Véhicule sur chambre'),
        ('303', '303 - Abonné absent'),
        ('3902', '3902 - PM vandalisé'),
        ('3202', '3202 - Pas d\'intervention nécessaire'),
    ]

    # Liste des choix pour le champ synchro
    SYNCHRO_CHOICES = [
        ('OK', 'OK'),
        ('NOK', 'NOK'),
        ('Null', 'Null'),
    ]

    # Champs du modèle
    numero_jeton = models.CharField(max_length=100, unique=True, verbose_name="Numéro de jeton")
    date_intervention = models.DateField(verbose_name="Date d'intervention")
    heure_debut = models.TimeField(verbose_name="Heure de début")
    techniciens_initial = models.CharField(max_length=100, verbose_name="Technicien initial")
    techniciens_intervenant = models.CharField(max_length=100, blank=True, null=True, verbose_name="Technicien intervenant")
    nbr_nok = models.IntegerField(default=0, verbose_name="Nombre de NOK")
    nbr_ok = models.IntegerField(default=0, verbose_name="Nombre de OK")
    total_interventions = models.IntegerField(default=0, verbose_name="Total des interventions")
    ref_pm = models.CharField(max_length=100, verbose_name="Référence PM")
    status_intervention = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="Statut de l'intervention")
    secteur = models.CharField(max_length=10, verbose_name="Secteur")
    secu = models.TextField(blank=True, null=True, verbose_name="Sécurité")
    heure_demarrage = models.TimeField(blank=True, null=True, verbose_name="Heure de démarrage")
    heure_cloture = models.TimeField(blank=True, null=True, verbose_name="Heure de clôture")
    synchro = models.CharField(max_length=10, choices=SYNCHRO_CHOICES, blank=True, null=True, verbose_name="Synchro")
    resultat_jj = models.TextField(blank=True, null=True, verbose_name="Résultat JJ")

    def __str__(self):
        return f"Intervention {self.numero_jeton} - {self.date_intervention}"

    class Meta:
        verbose_name = "Intervention SAV"
        verbose_name_plural = "Interventions SAV"


#inter Racc=================================================================================

from django.db import models

class InterventionsRACC(models.Model):
    # Choix pour le champ "Dernier Echec"
    DERNIER_ECHEC_CHOICES = [
        ('Client absent', 'Client absent'),
        ('Freebox non reçue', 'Freebox non reçue'),
        ('Client réalise les travaux', 'Client réalise les travaux'),
        ('Autorisation propriétaire', 'Autorisation propriétaire'),
        ('Accès refusé (Syndic/Copro)', 'Accès refusé (Syndic/Copro)'),
        ('Pas d accès PBO', 'Pas d accès PBO'),
        ('Manque de consommable', 'Manque de consommable'),
        ('Pas d Accès PM', 'Pas d Accès PM'),
        ('Autorisation du propriétaire', 'Autorisation du propriétaire'),
        ('RDV non honoré', 'RDV non honoré'),
        ('Fourreau à déboucher (intérieur)', 'Fourreau à déboucher (intérieur)'),
        ('Kit laissé mais non scanné', 'Kit laissé mais non scanné'),
        ('Refus d accès abonné', 'Refus d accès abonné'),
        # Ajoutez d'autres choix si nécessaire
    ]

    # Choix pour le champ "synchro"
    SYNCHRO_CHOICES = [
        ('OK', 'OK'),
        ('NOK', 'NOK'),
        ('Null', 'Null'),
    ]

    # Champs du modèle
    numero_jeton = models.CharField(max_length=100, unique=True)
    date_intervention = models.DateField()
    heure_debut = models.TimeField()
    techniciens_initial = models.CharField(max_length=100)
    techniciens_intervenant = models.CharField(max_length=100, blank=True, null=True)
    nbr_nok = models.IntegerField(default=0)
    nbr_ok = models.IntegerField(default=0)
    total_interventions = models.IntegerField(default=0)
    ref_pm = models.CharField(max_length=100)
    dernier_echec = models.CharField(max_length=100, choices=DERNIER_ECHEC_CHOICES, blank=True, null=True)
    secteur = models.CharField(max_length=10)
    contre_appel_client = models.TextField(blank=True, null=True)
    secu = models.TextField(blank=True, null=True)
    heure_demarrage = models.DateTimeField(blank=True, null=True)
    heure_cloture = models.DateTimeField(blank=True, null=True)
    synchro = models.CharField(max_length=10, choices=SYNCHRO_CHOICES, blank=True, null=True)
    resultat_jj = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Intervention RACC - {self.numero_jeton}"

    class Meta:
        verbose_name = "Intervention RACC"
        verbose_name_plural = "Interventions RACC"


# Commentaire ===================================================================================


from django.db import models
from django.utils import timezone
from core.models import RelanceJJ

class Commentaire(models.Model):
    jeton = models.ForeignKey(
        RelanceJJ,
        on_delete=models.CASCADE,
        verbose_name="RelanceJJ associé",  # Référence l'objet entier
        related_name="commentaires"
    )
    commentaire = models.TextField(verbose_name="Commentaire")
    commentateur = models.ForeignKey(
        'core.CustomUser',  # Référence explicite vers CustomUser
        on_delete=models.CASCADE,
        verbose_name="Commentateur"
    )
    created_date = models.DateField(verbose_name="Date du commentaire", blank=True, null=True)
    created_time = models.TimeField(verbose_name="Heure du commentaire", blank=True, null=True)
    
    def save(self, *args, **kwargs):
        now = timezone.now()
        # Utiliser la date_rdv de la relance si elle est définie, sinon la date actuelle
        if not self.created_date:
            self.created_date = self.jeton.date_rdv or now.date()
        if not self.created_time:
            self.created_time = now.time()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Commentaire par {self.commentateur.username} sur le jeton {self.jeton.jeton_commande}"



# models.py

from django.db import models
from django.conf import settings

class ImportARDLog(models.Model):
    fichier_nom = models.CharField(max_length=255)
    import_date = models.DateTimeField(auto_now_add=True)
    duree = models.FloatField(help_text="Durée en secondes")
    resultat = models.TextField(help_text="Log brut du traitement")
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.fichier_nom} - {self.import_date.strftime('%Y-%m-%d %H:%M')}"



