from django.core.management.base import BaseCommand
from core.models import RelanceJJ, ARD2, ControlPhoto, Parametres, DebriefRACC

class Command(BaseCommand):
    help = (
        "Synchronise les données de RelanceJJ (activite=RACC) + ARD2 (etat=NOK) "
        "dans DebriefRACC selon le mapping défini."
    )

    def handle(self, *args, **kwargs):
        relances = RelanceJJ.objects.filter(activite="RACC")
        self.stdout.write(self.style.NOTICE(f"Relances RACC détectées : {relances.count()}"))

        compteur = 0

        for relance in relances:
            # Vérifie que ARD2 associé existe et est NOK
            ard2 = ARD2.objects.filter(jeton_commande=relance.jeton_commande, etat_intervention="NOK").first()
            if not ard2:
                continue

            # Control à froid (ControlPhoto) pour appel_tech & resultat_controle
            control_photo = ControlPhoto.objects.filter(jeton=relance.jeton_commande).first()

            # Parametres pour numéro technicien et manager
            parametre = Parametres.objects.filter(numero_technicien=relance.numero).first()

            # Calcul du champ synchro selon conditions combinées
            if relance.statut == "Cloturée" and ard2.etat_intervention == "NOK":
                synchro_value = "Echec"
            elif relance.statut == "Taguée":
                synchro_value = "Taguées"
            else:
                synchro_value = ""

            # Préparation des données à injecter
            defaults = {
                "jeton": relance.jeton_commande,
                "date": relance.date_rdv,
                "tech": relance.techniciens,
                "numero_technicien": relance.numero,
                "secteur": relance.departement,
                "zone_manager": parametre.zone if parametre else None,
                "reference_pm": ard2.pm,
                "appel_tech": control_photo.statut_appel if control_photo else None,
                "synchro": synchro_value,
                "pec_par": control_photo.agent if control_photo else None,
                "resultat_controle": control_photo.resultats_verification if control_photo else None,
                "societe": relance.societe,
                "manager": parametre.manager if parametre else None,
                "nouveaux_tech": relance.techniciens,
                "code_cloture_technicien": "",
                "type_echec": "Echec client",  # Valeur par défaut, modifiable
                "diagnostic": "",
                "action": "",
            }

            # Création ou mise à jour de DebriefRACC
            instance, created = DebriefRACC.objects.update_or_create(
                jeton=relance.jeton_commande,
                defaults=defaults
            )

            compteur += 1
            self.stdout.write(self.style.SUCCESS(
                f"{'Créé' if created else 'Mis à jour'} : {relance.jeton_commande}"
            ))

        self.stdout.write(self.style.SUCCESS(f"Total synchronisés : {compteur}"))
