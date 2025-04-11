from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from core.models import ARD2, RelanceJJ, Gantt


class Command(BaseCommand):
    help = "Importe les interventions avec jetons dans Gantt"

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

        # Récupération des ARD2 du jour
        ard2_qs = ARD2.objects.filter(
            debut_intervention__date=intervention_date
        ) | ARD2.objects.filter(
            fin_intervention__date=intervention_date
        )

        gantt_data = {}
        now = timezone.localtime()

        for ard in ard2_qs:
            relance = RelanceJJ.objects.filter(jeton_commande=ard.jeton_commande).first()
            if not relance:
                self.stdout.write(self.style.WARNING(f"⚠️ Aucune RelanceJJ pour {ard.jeton_commande}"))
                continue

            activite = (relance.activite or "").upper()
            heure_prevue = relance.heure_prevue
            societe = relance.societe or ""

            hour = ard.debut_intervention.hour if ard.debut_intervention else (
                heure_prevue.hour if heure_prevue else 8
            )
            if hour < 8:
                hour = 8
            slot = f"heure_{min(hour, 18):02d}"
            jeton_slot = f"jeton_{min(hour, 18):02d}"  # Champ jeton correspondant

            statut_final = ""
            etat = (ard.etat_intervention or "").upper()

            if etat == "OK":
                if activite == "SAV":
                    statut_final = "OK SAV"
                elif activite == "RACC":
                    statut_final = "OK RACC"

            elif etat == "NOK":
                if ard.debut_intervention and ard.fin_intervention:
                    if activite == "SAV":
                        statut_final = "NOK SAV"
                    elif activite == "RACC":
                        statut_final = "NOK RACC"
                elif ard.debut_intervention and not ard.fin_intervention:
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
                self.stdout.write(self.style.WARNING(
                    f"❌ Pas de statut pour jeton {ard.jeton_commande} (état={etat}, activité={activite}, heure prévue={heure_prevue})"
                ))
                continue

            raw_tech = relance.techniciens or ard.technicien or "TECH INCONNU"
            if "," in raw_tech:
                technicien = raw_tech.split(",")[1].strip()
            else:
                technicien = raw_tech.strip()

            if technicien not in gantt_data:
                gantt_data[technicien] = {
                    "secteur": int(ard.departement) if ard.departement and ard.departement.isdigit() else 0,
                    "departement": ard.departement or "",
                    "nom_intervenant": technicien,
                    "societe": societe,
                    "interventions": {},
                    "jetons": {}  # Nouveau dictionnaire pour les jetons
                }

            gantt_data[technicien]["interventions"][slot] = statut_final
            gantt_data[technicien]["jetons"][jeton_slot] = ard.jeton_commande  # Ajout du jeton

        # Compléter avec les RelanceJJ sans intervention ARD2
        relances_planifiees = RelanceJJ.objects.filter(
            date_rdv=intervention_date,
            heure_debut__isnull=True,
            heure_fin__isnull=True,
            heure_prevue__isnull=False,
        ).exclude(
            jeton_commande__in=[ard.jeton_commande for ard in ard2_qs]
        )

        for relance in relances_planifiees:
            activite = (relance.activite or "").upper()
            societe = relance.societe or ""
            raw_tech = relance.techniciens or "TECH INCONNU"

            if "," in raw_tech:
                technicien = raw_tech.split(",")[1].strip()
            else:
                technicien = raw_tech.strip()

            heure_prevue = relance.heure_prevue
            heure_ref = datetime.combine(intervention_date, heure_prevue).replace(tzinfo=timezone.get_current_timezone())

            statut_final = "ALERTE RACC" if now > heure_ref else "PLANIFIÉE RACC"
            if activite == "SAV":
                statut_final = "ALERTE SAV" if now > heure_ref else "PLANIFIÉE SAV"

            hour = heure_prevue.hour if heure_prevue.hour >= 8 else 8
            slot = f"heure_{min(hour, 18):02d}"
            jeton_slot = f"jeton_{min(hour, 18):02d}"

            if technicien not in gantt_data:
                gantt_data[technicien] = {
                    "secteur": 0,
                    "departement": relance.departement or "",
                    "nom_intervenant": technicien,
                    "societe": societe,
                    "interventions": {},
                    "jetons": {}
                }

            current_status = gantt_data[technicien]["interventions"].get(slot, "")
            if not current_status or any(x in current_status for x in ["PLANIFIÉE", "ALERTE"]):
                gantt_data[technicien]["interventions"][slot] = statut_final
                gantt_data[technicien]["jetons"][jeton_slot] = relance.jeton_commande  # Ajout du jeton
                self.stdout.write(self.style.NOTICE(f"📝 {statut_final} ajouté pour {technicien} à {slot} (jeton: {relance.jeton_commande})"))
            else:
                self.stdout.write(self.style.NOTICE(f"⏭️ Slot {slot} pour {technicien} déjà rempli, non écrasé."))

        # Enregistrement dans Gantt
        with transaction.atomic():
            for tech, data in gantt_data.items():
                horaires = {}
                jetons = {}
                
                for i in range(8, 19):
                    h_key = f"heure_{i:02d}"
                    j_key = f"jeton_{i:02d}"
                    
                    # Gestion des statuts
                    new_statut = data["interventions"].get(h_key, "")
                    old_statut = getattr(gantt_obj, h_key) if gantt_obj else ""
                    horaires[h_key] = new_statut if new_statut else old_statut
                    
                    # Gestion des jetons
                    new_jeton = data["jetons"].get(j_key, "")
                    old_jeton = getattr(gantt_obj, j_key) if gantt_obj else ""
                    jetons[j_key] = new_jeton if new_jeton else old_jeton

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
                        **jetons,  # Ajout des jetons dans la mise à jour
                        "taux_transfo": taux_transfo,
                        "taux_remplissage": taux_remplissage,
                    }
                )
                action = "🆕 Créé" if created else "✅ Mis à jour"
                self.stdout.write(self.style.SUCCESS(f"{action} Gantt pour {tech} - {date_str}"))

        self.stdout.write(self.style.SUCCESS("🚀 Importation Gantt avec jetons terminée."))