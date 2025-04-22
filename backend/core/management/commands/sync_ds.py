from django.core.management.base import BaseCommand
from django.utils.timezone import now
from core.models import RelanceJJ, ARD2, ControlPhoto, Parametres, DebriefSAV, GRDV

class Command(BaseCommand):
    help = (
        "Synchronise uniquement les données de RelanceJJ (activite=SAV, statut=Cloturée, date=AUJOURD'HUI) "
        "avec ARD2 (etat=NOK) dans DebriefSAV selon le mapping défini."
    )

    def handle(self, *args, **kwargs):
        today = now().date()
        compteur = 0

        # ✅ Étape 1 : ne prendre que les SAV du jour, Cloturées
        relances = RelanceJJ.objects.filter(
            activite="SAV",
            statut="Cloturée",
            date_rdv=today
        ).select_related("grdv")

        self.stdout.write(self.style.NOTICE(f"Relances SAV Cloturées pour aujourd’hui : {relances.count()}"))

        for relance in relances:
            # ✅ Étape 2 : ne prendre que si ARD2 est NOK
            ard2 = ARD2.objects.filter(
                jeton_commande=relance.jeton_commande,
                etat_intervention="NOK"
            ).first()
            if not ard2:
                continue

            control_photo = ControlPhoto.objects.filter(jeton=relance.jeton_commande).first()
            parametre = Parametres.objects.filter(numero_technicien=relance.numero).first()
            grdv = relance.grdv

            # ✅ Synchro est toujours "Echec" ici
            synchro_value = "Echec"

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

            instance = DebriefSAV.objects.filter(jeton=relance).first()

            if instance:
                for key, value in defaults.items():
                    setattr(instance, key, value)
                instance.save()
                created = False
            else:
                instance = DebriefSAV.objects.create(jeton=relance, **defaults)
                created = True

            compteur += 1
            self.stdout.write(self.style.SUCCESS(
                f"{'Créé' if created else 'Mis à jour'} : {relance.jeton_commande}"
            ))

        self.stdout.write(self.style.SUCCESS(f"✅ Total synchronisés aujourd’hui (SAV + Cloturée + NOK) : {compteur}"))
