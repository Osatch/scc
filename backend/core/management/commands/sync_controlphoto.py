from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import RelanceJJ, ControlPhoto, ARD2


class Command(BaseCommand):
    help = (
        "Synchronise uniquement les données de RelanceJJ dont l'activité est RACC et la date est aujourd'hui.\n"
        "Si une entrée existe déjà pour le même jeton et la même date, elle est mise à jour.\n"
        "Sinon, une nouvelle est créée."
    )

    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        relances = RelanceJJ.objects.filter(activite="RACC", date_rdv=today)

        self.stdout.write(self.style.NOTICE(
            f"Nombre de RelanceJJ pour aujourd'hui ({today}) avec activité RACC : {relances.count()}"
        ))

        ard2_map = {a.jeton_commande: a for a in ARD2.objects.all()}
        cp_existing = {
            (c.jeton, c.date): c
            for c in ControlPhoto.objects.filter(date=today)
        }

        to_create = []
        to_update = []
        created = 0
        updated = 0

        for relance in relances:
            jeton = relance.jeton_commande
            date_rdv = relance.date_rdv

            if not jeton or not date_rdv:
                self.stdout.write(self.style.WARNING(f"RelanceJJ {relance.id} ignorée (jeton ou date manquant)."))
                continue

            ard = ard2_map.get(jeton)

            defaults = {
                "heure": relance.heure_prevue,
                "tech": relance.techniciens,
                "numero": relance.numero,
                "groupe_tech": "G1",
                "actif_depuis": date_rdv,
                "zone_manager": "#N/A",
                "statut": relance.statut,
                "secteur": relance.departement,
                "societe": relance.societe,
                "synchro": ard.etat_intervention if ard else None,
            }

            key = (jeton, date_rdv)
            if key in cp_existing:
                instance = cp_existing[key]
                for field, value in defaults.items():
                    setattr(instance, field, value)
                to_update.append(instance)
                updated += 1
                action = "Mis à jour"
            else:
                instance = ControlPhoto(jeton=jeton, date=date_rdv, **defaults)
                to_create.append(instance)
                created += 1
                action = "Créé"

            self.stdout.write(self.style.SUCCESS(f"{action} ControlPhoto pour jeton {jeton}, date {date_rdv}"))

        if to_create:
            ControlPhoto.objects.bulk_create(to_create, batch_size=100)
        if to_update:
            ControlPhoto.objects.bulk_update(
                to_update,
                fields=[
                    "heure", "tech", "numero", "groupe_tech", "actif_depuis", "zone_manager",
                    "statut", "secteur", "societe", "synchro"
                ],
                batch_size=100
            )

        self.stdout.write(self.style.NOTICE(f"Terminé : {created} créés, {updated} mis à jour."))
