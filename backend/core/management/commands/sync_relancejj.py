import unicodedata
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import GRDV, ARD2, RelanceJJ, Parametres


class Command(BaseCommand):
    help = (
        "Synchronise GRDV + ARD2 dans RelanceJJ uniquement pour la date du jour.\n"
        "- Mise à jour ou création selon jeton_commande + date.\n"
        "- Met à jour heure_prevue, heure_debut, heure_fin, statut, activité, numéro, société.\n"
        "- Optimisé pour exécution rapide."
    )

    def handle(self, *args, **kwargs):
        today = timezone.localdate()

        # Préchargement ARD2 (filtré pour aujourd'hui)
        ard2_map = {
            unicodedata.normalize("NFKC", a.jeton_commande.strip())[:10]: a
            for a in ARD2.objects.filter(date_rendez_vous__date=today)
        }

        # Préchargement Parametres (clé : (technicien, département))
        param_map = {
            (p.nom_tech.lower(), p.departement.lower()): p
            for p in Parametres.objects.all()
        }

        # Préchargement GRDV (filtré pour aujourd'hui)
        grdv_qs = GRDV.objects.filter(date_rdv__date=today)
        self.stdout.write(self.style.NOTICE(f"📋 GRDV trouvés pour {today} : {grdv_qs.count()}"))

        count_created = 0
        count_updated = 0
        relance_to_update = []
        relance_to_create = []

        # Relances existantes
        existing_relances = {
            (r.jeton_commande, r.date_rdv): r
            for r in RelanceJJ.objects.filter(date_rdv=today)
        }

        for grdv in grdv_qs:
            if not grdv.ref_commande:
                continue

            jeton = unicodedata.normalize("NFKC", grdv.ref_commande.strip())[:10]
            ard2 = ard2_map.get(jeton)
            if not ard2:
                continue

            # Heures
            heure_prevue = grdv.date_rdv.time() if grdv.date_rdv else None
            heure_debut = ard2.debut_intervention.time() if ard2.debut_intervention else None
            heure_fin = ard2.fin_intervention.time() if ard2.fin_intervention else None

            # Statut
            if heure_fin:
                statut = "Cloturée"
            elif heure_debut:
                statut = "Taguée"
            else:
                statut = ""

            # Activité (selon règle métier)
            activite = "SAV" if grdv.activite and "RDV-Sav" in grdv.activite else "RACC"

            key = (jeton, today)
            relance_obj = existing_relances.get(key)

            data_common = {
                "grdv": grdv,
                "activite": activite,
                "heure_prevue": heure_prevue,
                "heure_debut": heure_debut,
                "heure_fin": heure_fin,
                "departement": ard2.departement or '',
                "techniciens": ard2.technicien or '',
                "synchro": ard2.etat_intervention or '',
                "statut": statut,
            }

            if relance_obj:
                for field, value in data_common.items():
                    setattr(relance_obj, field, value)
                count_updated += 1
            else:
                relance_obj = RelanceJJ(
                    jeton_commande=jeton,
                    date_rdv=today,
                    **data_common
                )
                existing_relances[key] = relance_obj
                count_created += 1

            # Infos Parametres
            tech_key = (relance_obj.techniciens.lower(), relance_obj.departement.lower())
            param = param_map.get(tech_key)

            if param:
                if param.numero_technicien:
                    relance_obj.numero = param.numero_technicien
                if param.societe:
                    relance_obj.societe = param.societe

            if relance_obj.pk:
                relance_to_update.append(relance_obj)
            else:
                relance_to_create.append(relance_obj)

        # Écriture en base
        if relance_to_create:
            RelanceJJ.objects.bulk_create(relance_to_create, batch_size=1000)

        if relance_to_update:
            RelanceJJ.objects.bulk_update(
                relance_to_update,
                fields=[
                    "grdv", "activite", "heure_prevue", "heure_debut", "heure_fin",
                    "departement", "techniciens", "synchro", "statut",
                    "numero", "societe"
                ],
                batch_size=1000
            )

        # Résumé final
        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Synchronisation terminée pour {today} : {count_created} créés, {count_updated} mis à jour."
        ))
