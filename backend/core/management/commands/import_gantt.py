import unicodedata
from datetime import time
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from core.models import ARD2, RelanceJJ, Gantt

class Command(BaseCommand):
    help = "Importe les interventions d'ARD2 et RelanceJJ dans Gantt pour une journée donnée."

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help="Date des interventions au format YYYY-MM-DD (par défaut aujourd'hui)"
        )

    def handle(self, *args, **options):
        # Détermination de la date à traiter
        date_str = options.get('date')
        if date_str:
            try:
                intervention_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR("Format de date invalide. Utilisez YYYY-MM-DD."))
                return
        else:
            intervention_date = timezone.localdate()

        self.stdout.write(self.style.NOTICE(f"Début de l'importation dans Gantt pour le {intervention_date}..."))

        # Récupérer les interventions de la journée (ARD2) dont le champ debut_intervention est défini
        ard2_qs = ARD2.objects.filter(debut_intervention__date=intervention_date)
        if not ard2_qs.exists():
            self.stdout.write(self.style.WARNING(f"Aucune intervention trouvée pour le {intervention_date}."))
            return

        # Regrouper les données par technicien
        gantt_data = {}
        for ard in ard2_qs:
            # On ignore les interventions sans heure de début
            if not ard.debut_intervention:
                continue

            # Récupérer l'enregistrement RelanceJJ associé à cette intervention, si disponible
            relance = RelanceJJ.objects.filter(jeton_commande=ard.jeton_commande).first()

            # Déterminer le créneau horaire en fonction de l'heure de début
            hour = ard.debut_intervention.hour
            if 8 <= hour <= 15:
                slot = f"heure_{hour:02d}"
                base_status = ard.etat_intervention.upper() if ard.etat_intervention else ""
                if relance:
                    activite = getattr(relance, "activite", "")
                    activite = activite.upper() if activite else ""
                    statut = getattr(relance, "statut", "")
                    statut = statut.lower() if statut else ""
                    status_str = f"{base_status} {activite}".strip()
                    if statut == "taguée":
                        status_str += " EN COURS"
                else:
                    status_str = base_status
            elif hour in [16, 17] or hour >= 18:
                slot = "heure_18" if hour >= 18 else f"heure_{hour:02d}"
                status_str = ard.etat_intervention.upper() if ard.etat_intervention else ""
            else:
                continue

            technicien = ard.technicien
            # Initialiser les données pour ce technicien pour ce jour
            if technicien not in gantt_data:
                gantt_data[technicien] = {
                    "secteur": ard.departement,          # Conserve secteur/département si besoin
                    "departement": ard.departement,
                    "nom_intervenant": technicien,
                    "heure_08": "",
                    "heure_09": "",
                    "heure_10": "",
                    "heure_11": "",
                    "heure_12": "",
                    "heure_13": "",
                    "heure_14": "",
                    "heure_15": "",
                    "heure_16": "",
                    "heure_17": "",
                    "heure_18": "",
                    "interventions": {}
                }
            # Concaténer les interventions dans le même créneau si nécessaire (séparées par "; ")
            current_val = gantt_data[technicien]["interventions"].get(slot, "")
            new_val = current_val + "; " + status_str if current_val else status_str
            gantt_data[technicien]["interventions"][slot] = new_val

        # Mise à jour / création des enregistrements Gantt
        with transaction.atomic():
            for technicien, data in gantt_data.items():
                horaires = {
                    "heure_08": data["interventions"].get("heure_08", ""),
                    "heure_09": data["interventions"].get("heure_09", ""),
                    "heure_10": data["interventions"].get("heure_10", ""),
                    "heure_11": data["interventions"].get("heure_11", ""),
                    "heure_12": data["interventions"].get("heure_12", ""),
                    "heure_13": data["interventions"].get("heure_13", ""),
                    "heure_14": data["interventions"].get("heure_14", ""),
                    "heure_15": data["interventions"].get("heure_15", ""),
                    "heure_16": data["interventions"].get("heure_16", ""),
                    "heure_17": data["interventions"].get("heure_17", ""),
                    "heure_18": data["interventions"].get("heure_18", ""),
                }

                # Calcul des indicateurs
                ok_count = 0
                filled_cells = 0
                for val in horaires.values():
                    if val:
                        filled_cells += 1
                        if val.upper().startswith("OK"):
                            ok_count += 1
                taux_transfo = (ok_count / filled_cells * 100) if filled_cells > 0 else 0

                total_slots = 11
                filled_total = sum(1 for v in horaires.values() if v)
                taux_remplissage = (filled_total / total_slots * 100)

                # Ici, update_or_create utilise nom_intervenant et date_intervention pour éviter les doublons
                gantt_obj, created = Gantt.objects.update_or_create(
                    nom_intervenant=data["nom_intervenant"],
                    date_intervention=intervention_date,
                    defaults={
                        "secteur": data["secteur"],
                        "departement": data["departement"],
                        "heure_08": horaires["heure_08"],
                        "heure_09": horaires["heure_09"],
                        "heure_10": horaires["heure_10"],
                        "heure_11": horaires["heure_11"],
                        "heure_12": horaires["heure_12"],
                        "heure_13": horaires["heure_13"],
                        "heure_14": horaires["heure_14"],
                        "heure_15": horaires["heure_15"],
                        "heure_16": horaires["heure_16"],
                        "heure_17": horaires["heure_17"],
                        "heure_18": horaires["heure_18"],
                        "taux_transfo": taux_transfo,
                        "taux_remplissage": taux_remplissage,
                    }
                )
                action = "Créé" if created else "Mis à jour"
                self.stdout.write(self.style.SUCCESS(f"{action} Gantt pour {data['nom_intervenant']} - {intervention_date}"))

        self.stdout.write(self.style.SUCCESS("Importation terminée."))
