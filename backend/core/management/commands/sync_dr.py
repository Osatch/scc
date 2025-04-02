import unicodedata
from django.core.management.base import BaseCommand
from core.models import RelanceJJ, DebriefRACC, ARD2  # ajuste le chemin selon ton projet

class Command(BaseCommand):
    help = (
        "Synchronise les données de RelanceJJ et ARD2 vers DebriefRACC "
        "(uniquement si activite='RACC' et ARD2.etat_intervention='NOK')."
    )

    def handle(self, *args, **kwargs):
        relances = RelanceJJ.objects.filter(activite="RACC", jeton__etat_intervention="NOK")
        self.stdout.write(self.style.NOTICE(f"Nombre de RelanceJJ valides (RACC & NOK): {relances.count()}"))

        for relance in relances:
            # On récupère le lien ARD2 depuis le jeton
            ard2 = relance.jeton

            if not ard2:
                self.stdout.write(self.style.WARNING(f"Aucun ARD2 pour jeton {relance.jeton_commande}, on saute."))
                continue

            # Préparer les valeurs par défaut pour création ou mise à jour
            defaults = {
                "nouveaux_tech": relance.techniciens,
                "pec_par": relance.pec,
                "resultat_controle": "null",
                "appel_tech": "null",
                "synchro": "Taguées",  # valeur personnalisée selon ton besoin
                "type_echec": "null",
                "diagnostic": "",
                "code_cloture_technicien": "",
            }

            # Chercher s'il existe déjà un DebriefRACC lié à cette relance
            debrief = DebriefRACC.objects.filter(relance=relance).first()

            if debrief:
                for key, value in defaults.items():
                    setattr(debrief, key, value)
                debrief.save()
                action = "Mis à jour"
            else:
                DebriefRACC.objects.create(relance=relance, **defaults)
                action = "Créé"

            self.stdout.write(self.style.SUCCESS(
                f"{action} DebriefRACC pour jeton {relance.jeton_commande}"
            ))
