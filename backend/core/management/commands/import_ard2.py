import csv
import os
import glob
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from core.models import ARD2


class Command(BaseCommand):
    help = (
        "Import optimisé du dernier fichier CSV ARD2 :\n"
        "- Mise à jour si jeton existe et RDV vide ou même date\n"
        "- Sinon, création d’un nouvel enregistrement.\n"
        "- Importe correctement `date_rendez_vous`, `debut_intervention`, `fin_intervention`."
    )

    def parse_date(self, date_str):
        if not date_str:
            return None
        formats = [
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M",
            "%Y-%m-%d %H:%M:%S",  # Format ISO
            "%Y-%m-%d %H:%M"
        ]
        for fmt in formats:
            try:
                parsed = datetime.strptime(date_str, fmt)
                return make_aware(parsed)
            except Exception:
                continue
        return None

    def handle(self, *args, **options):
        csv_dir = os.path.join(settings.BASE_DIR, "Bot", "ard2")
        csv_pattern = os.path.join(csv_dir, "*.csv")
        csv_files = glob.glob(csv_pattern)

        if not csv_files:
            self.stdout.write(self.style.ERROR(f"Aucun fichier CSV trouvé dans {csv_dir}."))
            return

        latest_file = max(csv_files, key=os.path.getmtime)
        self.stdout.write(self.style.WARNING(f"📄 Fichier CSV détecté : {latest_file}"))

        try:
            with open(latest_file, mode='r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                print("✅ Colonnes détectées :", reader.fieldnames)

                now = make_aware(datetime.now())
                total_lignes = 0
                updated = 0
                created = 0
                skipped = 0
                errors = 0

                # Chargement des ARD2 existants
                existing_ard2 = {
                    a.jeton_commande: a for a in ARD2.objects.all()
                }

                objets_a_mettre_a_jour = []
                objets_a_creer = []

                for index, row in enumerate(reader, start=2):
                    total_lignes += 1
                    row = {k.strip().lower(): v.strip() for k, v in row.items() if k}

                    jeton = row.get('jeton_commande') or row.get('jeton de commande')
                    rdv_str = row.get("date_rendez_vous") or row.get("date du rendez-vous")
                    debut_str = row.get("debut_intervention") or row.get("début d'intervention")
                    fin_str = row.get("fin_intervention") or row.get("fin d'intervention")
                    terminee_val = row.get("terminee") or row.get("terminée")
                    etat = row.get("etat_intervention") or row.get("état de l'intervention")
                    techniciens = row.get("techniciens")
                    departement = row.get("departement") or row.get("département")
                    pm = row.get("pm")

                    if not jeton or not rdv_str:
                        skipped += 1
                        continue

                    date_rendez_vous = self.parse_date(rdv_str)
                    debut_intervention = self.parse_date(debut_str)
                    fin_intervention = self.parse_date(fin_str)
                    terminee = terminee_val.upper() == 'OUI' if terminee_val else False

                    if not date_rendez_vous:
                        self.stdout.write(self.style.ERROR(
                            f"❌ Ligne {index} : date_rendez_vous invalide : '{rdv_str}'"))
                        errors += 1
                        continue

                    instance_existante = existing_ard2.get(jeton)
                    if instance_existante:
                        if not instance_existante.date_rendez_vous or (
                            instance_existante.date_rendez_vous.date() == date_rendez_vous.date()
                        ):
                            instance_existante.date_rendez_vous = date_rendez_vous
                            instance_existante.debut_intervention = debut_intervention
                            instance_existante.fin_intervention = fin_intervention
                            instance_existante.terminee = terminee
                            instance_existante.etat_intervention = etat or ""
                            instance_existante.technicien = techniciens or ""
                            instance_existante.departement = departement or ""
                            instance_existante.pm = pm or ""
                            instance_existante.date_importation = now
                            objets_a_mettre_a_jour.append(instance_existante)
                            updated += 1
                        else:
                            skipped += 1
                    else:
                        nouveau = ARD2(
                            jeton_commande=jeton,
                            date_rendez_vous=date_rendez_vous,
                            debut_intervention=debut_intervention,
                            fin_intervention=fin_intervention,
                            terminee=terminee,
                            etat_intervention=etat or "",
                            technicien=techniciens or "",
                            departement=departement or "",
                            pm=pm or "",
                            date_importation=now,
                        )
                        objets_a_creer.append(nouveau)
                        created += 1

                # Sauvegardes en batch
                if objets_a_mettre_a_jour:
                    ARD2.objects.bulk_update(
                        objets_a_mettre_a_jour,
                        [
                            'date_rendez_vous', 'debut_intervention', 'fin_intervention',
                            'terminee', 'etat_intervention', 'technicien',
                            'departement', 'pm', 'date_importation'
                        ],
                        batch_size=1000
                    )

                if objets_a_creer:
                    ARD2.objects.bulk_create(objets_a_creer, batch_size=1000)

                # Résumé
                self.stdout.write(self.style.SUCCESS("✅ Import terminé."))
                self.stdout.write(self.style.SUCCESS(f"📄 Lignes lues : {total_lignes}"))
                self.stdout.write(self.style.SUCCESS(f"✅ Créés : {created}"))
                self.stdout.write(self.style.SUCCESS(f"♻️ Mis à jour : {updated}"))
                self.stdout.write(self.style.WARNING(f"➖ Ignorés (doublons hors date) : {skipped}"))
                self.stdout.write(self.style.ERROR(f"❌ Erreurs parsing dates : {errors}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR("❌ Erreur lors de l'import :"))
            self.stdout.write(self.style.ERROR(str(e)))
