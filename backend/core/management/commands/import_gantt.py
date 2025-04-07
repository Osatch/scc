from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from core.models import ARD2, RelanceJJ, Gantt


class Command(BaseCommand):
    help = "Importe les interventions d'ARD2 et RelanceJJ dans Gantt pour une journée donnée (YYYY-MM-DD)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help="Date au format YYYY-MM-DD (par défaut aujourd'hui)"
        )

    def handle(self, *args, **options):
        date_str = options.get('date')
        if date_str:
            try:
                intervention_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR("Format de date invalide. Utilisez YYYY-MM-DD."))
                return
        else:
            intervention_date = timezone.localdate()
            date_str = intervention_date.strftime('%Y-%m-%d')

        self.stdout.write(self.style.NOTICE(f"📆 Import Gantt pour le {date_str}"))

        ard2_qs = ARD2.objects.filter(debut_intervention__date=intervention_date)
        if not ard2_qs.exists():
            self.stdout.write(self.style.WARNING(f"Aucune intervention ARD2 trouvée pour {date_str}"))
            return

        gantt_data = {}
        now = timezone.localtime()

        for ard in ard2_qs:
            relance = RelanceJJ.objects.filter(jeton_commande=ard.jeton_commande).first()
            activite = (relance.activite or "").upper() if relance else ""
            heure_prevue = relance.heure_prevue if relance else None
            societe = relance.societe if relance else ""

            hour = ard.debut_intervention.hour if ard.debut_intervention else (
                heure_prevue.hour if heure_prevue else None
            )

            if hour is None or hour < 8:
                continue

            slot = f"heure_{min(hour, 18):02d}"  # tout ce qui dépasse 18h va dans heure_18

            # ===== Logique de statut à afficher =====
            statut_final = ""
            etat = (ard.etat_intervention or "").upper()

            if etat == "OK":
                if activite == "SAV":
                    statut_final = "OK SAV"
                elif activite == "RACC":
                    statut_final = "OK RACC"

            elif etat == "NOK":
                if ard.fin_intervention:
                    if activite == "SAV":
                        statut_final = "NOK SAV"
                    elif activite == "RACC":
                        statut_final = "NOK RACC"
                elif not ard.fin_intervention:
                    if ard.debut_intervention:
                        if activite == "SAV":
                            statut_final = "EN COURS SAV"
                        elif activite == "RACC":
                            statut_final = "EN COURS RACC"
                    elif not ard.debut_intervention and heure_prevue:
                        heure_ref = datetime.combine(intervention_date, heure_prevue).replace(tzinfo=timezone.get_current_timezone())
                        if now > heure_ref:
                            statut_final = "ALERTE SAV" if activite == "SAV" else "ALERTE RACC"
                        else:
                            statut_final = "PLANIFIÉE SAV" if activite == "SAV" else "PLANIFIÉE RACC"

            if not statut_final:
                continue  # Ligne ignorée si statut non défini

            technicien = ard.technicien
            if technicien not in gantt_data:
                gantt_data[technicien] = {
                    "secteur": int(ard.departement) if ard.departement.isdigit() else 0,
                    "departement": ard.departement,
                    "nom_intervenant": technicien,
                    "societe": societe,
                    "interventions": {}
                }

            # ✅ Remplace l'ancien statut par le nouveau
            gantt_data[technicien]["interventions"][slot] = statut_final

        # Enregistrement dans Gantt
        with transaction.atomic():
            for tech, data in gantt_data.items():
                horaires = {
                    f"heure_{i:02d}": data["interventions"].get(f"heure_{i:02d}", "")
                    for i in range(8, 19)
                }

                ok_count = sum(1 for val in horaires.values() if "OK" in val.upper())
                filled_count = sum(1 for val in horaires.values() if val)
                taux_transfo = (ok_count / filled_count * 100) if filled_count else 0
                taux_remplissage = (filled_count / 11 * 100)

                gantt_obj, created = Gantt.objects.update_or_create(
                    nom_intervenant=data["nom_intervenant"],
                    date_intervention=intervention_date,
                    defaults={
                        "secteur": data["secteur"],
                        "departement": data["departement"],
                        "societe": data["societe"],
                        **horaires,
                        "taux_transfo": taux_transfo,
                        "taux_remplissage": taux_remplissage,
                    }
                )
                action = "🆕 Créé" if created else "✅ Mis à jour"
                self.stdout.write(self.style.SUCCESS(f"{action} Gantt pour {tech} - {date_str}"))

        self.stdout.write(self.style.SUCCESS("🚀 Importation Gantt terminée."))
