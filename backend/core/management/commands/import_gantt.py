from datetime import datetime, time
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from core.models import ARD2, RelanceJJ, Gantt


class Command(BaseCommand):
    help = "Synchronise les interventions dans le Gantt en fonction de l'état réel (optimisé avec bulk_update)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help="Date de synchronisation au format YYYY-MM-DD (défaut : aujourd'hui)"
        )

    def handle(self, *args, **options):
        date_str = options.get('date')
        intervention_date = timezone.localdate() if not date_str else datetime.strptime(date_str, '%Y-%m-%d').date()

        self.stdout.write(self.style.NOTICE(f"\n📅 Synchronisation GANTT pour le {intervention_date}"))

        relances = list(RelanceJJ.objects.filter(date_rdv=intervention_date))
        interventions = {
            i.jeton_commande: i for i in ARD2.objects.filter(date_rendez_vous__date=intervention_date)
        }
        now = timezone.localtime()
        gantt_data = {}

        for relance in relances:
            jeton = relance.jeton_commande
            technicien = self.get_technicien(relance.techniciens)
            heure = max(8, min(self.get_creneau_horaire(relance), 18))
            slot = f"heure_{heure:02d}"
            jeton_slot = f"jeton_{heure:02d}"

            intervention = interventions.get(jeton)
            statut = self.get_statut(relance, intervention, now)
            if not statut:
                continue

            if technicien not in gantt_data:
                gantt_data[technicien] = {
                    "secteur": self.get_secteur(intervention, relance),
                    "departement": relance.departement or (intervention.departement if intervention else ""),
                    "nom_intervenant": technicien,
                    "societe": relance.societe or "",
                    "interventions": {},
                    "jetons": {},
                    "heure_debuts": {},
                    "heure_fins": {},
                    "total_interventions": 0,
                    "ok_count": 0,
                }

            if jeton in gantt_data[technicien]["jetons"].values():
                current_jeton = gantt_data[technicien]["jetons"].get(jeton_slot)
                if current_jeton != jeton:
                    self.stdout.write(self.style.WARNING(f"⛔ Jeton {jeton} déjà utilisé pour {technicien} – {slot} ignoré"))
                    continue

            if statut.startswith("EN COURS") and any(
                v.startswith("EN COURS") for v in gantt_data[technicien]["interventions"].values()
            ) and slot not in gantt_data[technicien]["interventions"]:
                self.stdout.write(self.style.WARNING(f"⛔ {technicien} a déjà une intervention EN COURS – {slot} ignoré"))
                continue

            current = gantt_data[technicien]["interventions"].get(slot, "")
            if not current or self.plus_prioritaire(statut, current):
                gantt_data[technicien]["interventions"][slot] = statut
                gantt_data[technicien]["jetons"][jeton_slot] = jeton
                gantt_data[technicien]["heure_debuts"][f"heure_debut_{heure:02d}"] = relance.heure_debut
                gantt_data[technicien]["heure_fins"][f"heure_fin_{heure:02d}"] = relance.heure_fin
                self.stdout.write(self.style.SUCCESS(f"🔄 {technicien} – {slot}: {current or 'VIDE'} → {statut}"))

            gantt_data[technicien]["total_interventions"] += 1
            if statut.startswith("OK"):
                gantt_data[technicien]["ok_count"] += 1

        self.save_gantt_bulk(gantt_data, intervention_date)
        self.stdout.write(self.style.SUCCESS("\n✅ Synchronisation GANTT terminée."))

    def save_gantt_bulk(self, gantt_data, date):
        with transaction.atomic():
            existing_map = {
                g.nom_intervenant: g
                for g in Gantt.objects.filter(date_intervention=date)
            }

            to_update = []
            to_create = []

            for tech, data in gantt_data.items():
                horaires = {f"heure_{h:02d}": "" for h in range(8, 19)}
                jetons = {f"jeton_{h:02d}": "" for h in range(8, 19)}
                heure_debuts = {f"heure_debut_{h:02d}": None for h in range(8, 19)}
                heure_fins = {f"heure_fin_{h:02d}": None for h in range(8, 19)}

                for h in range(8, 19):
                    slot = f"heure_{h:02d}"
                    jeton_slot = f"jeton_{h:02d}"
                    heure_debut_slot = f"heure_debut_{h:02d}"
                    heure_fin_slot = f"heure_fin_{h:02d}"

                    horaires[slot] = data["interventions"].get(slot, "")
                    jetons[jeton_slot] = data["jetons"].get(jeton_slot, "")
                    heure_debuts[heure_debut_slot] = data["heure_debuts"].get(heure_debut_slot)
                    heure_fins[heure_fin_slot] = data["heure_fins"].get(heure_fin_slot)

                total = data["total_interventions"]
                ok = data["ok_count"]
                taux_transfo = round((ok / total * 100), 2) if total else 0
                taux_remplissage = round((total / 5 * 100), 2)

                fields = {
                    "secteur": data["secteur"],
                    "departement": data["departement"],
                    "societe": data["societe"],
                    "taux_transfo": taux_transfo,
                    "taux_remplissage": taux_remplissage,
                    **horaires,
                    **jetons,
                    **heure_debuts,
                    **heure_fins,
                }

                if tech in existing_map:
                    gantt = existing_map[tech]
                    for k, v in fields.items():
                        setattr(gantt, k, v)
                    to_update.append(gantt)
                else:
                    to_create.append(Gantt(
                        nom_intervenant=tech,
                        date_intervention=date,
                        **fields
                    ))

            if to_create:
                Gantt.objects.bulk_create(to_create, batch_size=1000)

            if to_update:
                Gantt.objects.bulk_update(
                    to_update,
                    fields=[
                        "secteur", "departement", "societe",
                        "taux_transfo", "taux_remplissage"
                    ]
                    + [f"heure_{h:02d}" for h in range(8, 19)]
                    + [f"jeton_{h:02d}" for h in range(8, 19)]
                    + [f"heure_debut_{h:02d}" for h in range(8, 19)]
                    + [f"heure_fin_{h:02d}" for h in range(8, 19)],
                    batch_size=1000
                )

    def get_statut(self, relance, intervention, now):
        activite = (relance.activite or "SAV").upper()
        heure_prevue = relance.heure_prevue or time(8, 0)
        heure_datetime = datetime.combine(relance.date_rdv, heure_prevue).replace(tzinfo=timezone.get_current_timezone())

        if intervention:
            if intervention.fin_intervention:
                return f"OK {activite}" if intervention.etat_intervention == "OK" else f"NOK {activite}"
            if intervention.debut_intervention:
                return f"EN COURS {activite}"
        else:
            if relance.statut == "Cloturée":
                return f"OK {activite}"
            if relance.statut == "Taguée":
                return f"EN COURS {activite}"

        return f"ALERTE {activite}" if now > heure_datetime else f"PLANIFIÉE {activite}"

    def plus_prioritaire(self, new, old):
        ordre = ['OK', 'NOK', 'EN COURS', 'ALERTE', 'PLANIFIÉE']
        idx = lambda s: next((i for i, v in enumerate(ordre) if v in s), 999)
        return idx(new) < idx(old)

    def get_technicien(self, raw):
        name = (raw or "TECH INCONNU").strip()
        return name.split(",")[1].strip() if "," in name else name

    def get_creneau_horaire(self, relance):
        return (relance.heure_prevue or time(8, 0)).hour

    def get_secteur(self, intervention, relance):
        dep = intervention.departement if intervention else relance.departement
        return int(dep) if dep and dep.isdigit() else 0
