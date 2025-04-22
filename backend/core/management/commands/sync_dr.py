from django.core.management.base import BaseCommand
from django.utils.timezone import now
from core.models import RelanceJJ, ARD2, ControlPhoto, Parametres, DebriefRACC

class Command(BaseCommand):
    help = "Synchronise uniquement les RACC Cloturées avec ARD2 NOK dans DebriefRACC."

    def handle(self, *args, **kwargs):
        today = now().date()
        compteur = 0

        # 1. Filtrer les ARD2 NOK
        ard2_nok_map = {
            a.jeton_commande: a for a in ARD2.objects.filter(etat_intervention="NOK")
        }

        # 2. Filtrer les RelanceJJ du jour, Cloturées, RACC, et dont le jeton est dans ARD2 NOK
        relances = RelanceJJ.objects.filter(
            activite="RACC",
            statut="Cloturée",
            date_rdv=today,
            jeton_commande__in=ard2_nok_map.keys()
        )

        self.stdout.write(self.style.NOTICE(f"Relances filtrées (RACC + Cloturée + NOK) : {relances.count()}"))

        # 3. Préchargement pour optimisation
        controls = {
            cp.jeton: cp for cp in ControlPhoto.objects.filter(jeton__in=[r.jeton_commande for r in relances])
        }
        parametres = {
            p.numero_technicien: p for p in Parametres.objects.filter(
                numero_technicien__in=[r.numero for r in relances]
            )
        }

        for relance in relances:
            ard2 = ard2_nok_map.get(relance.jeton_commande)
            if not ard2:
                continue  # Sécurité

            control_photo = controls.get(relance.jeton_commande)
            parametre = parametres.get(relance.numero)

            defaults = {
                "jeton": relance.jeton_commande,
                "date": relance.date_rdv,
                "tech": relance.techniciens,
                "numero_technicien": relance.numero,
                "secteur": relance.departement,
                "zone_manager": parametre.zone if parametre else None,
                "reference_pm": ard2.pm,
                "appel_tech": control_photo.statut_appel if control_photo else None,
                "synchro": "Echec",
                "pec_par": control_photo.agent if control_photo else None,
                "resultat_controle": control_photo.resultats_verification if control_photo else None,
                "societe": relance.societe,
                "manager": parametre.manager if parametre else None,
                "nouveaux_tech": relance.techniciens,
                "code_cloture_technicien": "",
                "type_echec": "Echec client",
                "diagnostic": "",
                "action": "",
            }

            DebriefRACC.objects.update_or_create(
                jeton=relance.jeton_commande,
                defaults=defaults
            )

            compteur += 1
            self.stdout.write(self.style.SUCCESS(f"Enregistré : {relance.jeton_commande}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Total enregistrés (Cloturée + NOK + RACC) : {compteur}"))
