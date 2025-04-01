import unicodedata
from django.core.management.base import BaseCommand
from core.models import RelanceJJ, ControlPhoto, ARD2  # Assurez-vous que ARD2 est importé

class Command(BaseCommand):
    help = (
        "Synchronise les données de RelanceJJ dans ControlPhoto. "
        "Mapping : date = date_rdv, heure = heure_prevue, tech = techniciens, "
        "numero = numero, groupe_tech = 'G1' par défaut, actif_depuis = date_rdv, "
        "zone_manager = '#N/A', statut = statut, secteur = departement, "
        "societe = societe, synchro = etat_intervention d'ARD2 (si instance trouvée), "
        "jeton = jeton_commande de RelanceJJ."
    )

    def handle(self, *args, **kwargs):
        relances = RelanceJJ.objects.all()
        self.stdout.write(self.style.NOTICE(f"Nombre total de RelanceJJ : {relances.count()}"))

        for relance in relances:
            # Préparation des valeurs à mettre à jour/créer dans ControlPhoto
            defaults = {
                "jeton": relance.jeton_commande,  # Ajout direct du champ jeton
                "date": relance.date_rdv,
                "heure": relance.heure_prevue,
                "tech": relance.techniciens,
                "numero": relance.numero,
                "groupe_tech": "G1",              # Valeur par défaut (ajustez si nécessaire)
                "actif_depuis": relance.date_rdv,   # Utilise date_rdv comme date d'activité par défaut
                "zone_manager": "#N/A",           # Valeur par défaut
                "statut": relance.statut,
                "secteur": relance.departement,
                "societe": relance.societe,
            }

            # Récupération de l'instance ARD2 liée via jeton_commande
            ard_instance = ARD2.objects.filter(jeton_commande=relance.jeton_commande).first()
            if ard_instance:
                defaults["synchro"] = ard_instance.etat_intervention
            else:
                defaults["synchro"] = None  # ou définir une valeur par défaut

            # Recherche d'une instance ControlPhoto liée à ce RelanceJJ via jeton
            control_photo_instance = ControlPhoto.objects.filter(jeton=relance.jeton_commande).first()

            if control_photo_instance:
                # Mise à jour de l'instance existante
                for key, value in defaults.items():
                    setattr(control_photo_instance, key, value)
                control_photo_instance.save()
                action = "Mis à jour"
            else:
                # Création d'une nouvelle instance avec les valeurs par défaut
                control_photo_instance = ControlPhoto.objects.create(**defaults)
                action = "Créé"

            self.stdout.write(self.style.SUCCESS(
                f"{action} ControlPhoto pour RelanceJJ avec jeton {relance.jeton_commande}"
            ))
