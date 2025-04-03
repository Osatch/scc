from django.core.management.base import BaseCommand
from core.models import RelanceJJ, ARD2, ControlPhoto, Parametres, DebriefSAV, GRDV

class Command(BaseCommand):
    help = (
        "Synchronise les données de RelanceJJ (activite=RACC) + ARD2 (etat=NOK) "
        "dans DebriefSAV selon le mapping défini."
    )

    def handle(self, *args, **kwargs):
        relances = RelanceJJ.objects.filter(activite="RACC")
        self.stdout.write(self.style.NOTICE(f"Relances RACC détectées : {relances.count()}"))

        compteur = 0

        for relance in relances:
            # Ne traite que si ARD2 existe et NOK
            ard2 = ARD2.objects.filter(jeton_commande=relance.jeton_commande, etat_intervention="NOK").first()
            if not ard2:
                continue

            control_photo = ControlPhoto.objects.filter(jeton=relance.jeton_commande).first()
            parametre = Parametres.objects.filter(numero_technicien=relance.numero).first()
            grdv = relance.grdv

            # Détermine la valeur de synchronisation
            if relance.statut == "Cloturée" and ard2.etat_intervention == "NOK":
                synchro_value = "Echec"
            elif relance.statut == "Taguée":
                synchro_value = "Taguée"
            elif relance.statut == "Cloturée" and ard2.etat_intervention == "OK":
                synchro_value = "OK"
            else:
                synchro_value = ""

            defaults = {
                "date": relance.date_rdv,
                "heure": relance.heure_prevue,
                "tech": relance.techniciens,
                "numero_tech": relance.numero,
                "secteur": relance.departement,
                "zone_manager": parametre.zone if parametre else None,
                "reference_pm": ard2.pm if ard2 else None,
                "appel_tech": control_photo.statut_appel if control_photo else None,
                "synchro": synchro_value,
                "pec_par": control_photo.agent if control_photo else None,
                "resultat_controle": control_photo.resultats_verification if control_photo else None,
                "societe": relance.societe,
                "manager": parametre.manager if parametre else None,
                "tel_contact": grdv.tel_contact if grdv else None,
            }

            instance, created = DebriefSAV.objects.update_or_create(
                jeton=relance,
                defaults=defaults
            )

            compteur += 1
            self.stdout.write(self.style.SUCCESS(
                f"{'Créé' if created else 'Mis à jour'} : {relance.jeton_commande}"
            ))

        self.stdout.write(self.style.SUCCESS(f"Total synchronisés : {compteur}"))
