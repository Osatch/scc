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
        "Importe le dernier fichier CSV ARD2 dans la base de données.\n"
        "- Si une ligne existe avec le même jeton_commande ET aucune date, ou même date de début => mise à jour.\n"
        "- Sinon => création d'une nouvelle ligne."
    )

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
            with open(latest_file, mode='r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')

                imported_count = 0
                skipped_count = 0
                now = make_aware(datetime.now())

                for row in reader:
                    # Nettoyage des clés et valeurs
                    row = {k.strip().lower(): v.strip() for k, v in row.items() if k is not None}

                    jeton = row.get('jeton de commande')
                    debut_str = row.get("début d'intervention")
                    fin_str = row.get("fin d'intervention")
                    terminee_val = row.get("terminée")
                    etat = row.get("état de l'intervention")
                    techniciens = row.get("techniciens")
                    departement = row.get("département")
                    pm = row.get("pm")

                    if not jeton:
                        self.stdout.write(self.style.WARNING(f"⚠️ Ligne ignorée (jeton vide) : {row}"))
                        skipped_count += 1
                        continue

                    debut_intervention = self.parse_date(debut_str) if debut_str else None
                    fin_intervention = self.parse_date(fin_str) if fin_str else None

                    if debut_str and debut_intervention is None:
                        self.stdout.write(self.style.ERROR(f"❌ Erreur de conversion de la date pour la ligne : {row}"))
                        skipped_count += 1
                        continue

                    terminee = terminee_val.upper() == 'OUI' if terminee_val else False

                    try:
                        existing_entry = ARD2.objects.filter(jeton_commande=jeton).first()
                        should_update = False

                        if existing_entry:
                            if not existing_entry.debut_intervention:
                                should_update = True
                            elif debut_intervention and existing_entry.debut_intervention.date() == debut_intervention.date():
                                should_update = True

                        if existing_entry and should_update:
                            existing_entry.debut_intervention = debut_intervention
                            existing_entry.fin_intervention = fin_intervention
                            existing_entry.terminee = terminee
                            existing_entry.etat_intervention = etat if etat else ""
                            existing_entry.technicien = techniciens if techniciens else ""
                            existing_entry.departement = departement if departement else ""
                            existing_entry.pm = pm if pm else ""
                            existing_entry.date_importation = now
                            existing_entry.save()

                            self.stdout.write(self.style.SUCCESS(
                                f"✅ Jeton {jeton} mis à jour (date: {debut_intervention.date() if debut_intervention else 'N/A'})"
                            ))
                            imported_count += 1

                        elif existing_entry:
                            self.stdout.write(self.style.WARNING(
                                f"⚠️ Jeton {jeton} déjà existant mais pas sur la même journée → ligne ignorée."
                            ))
                            skipped_count += 1

                        else:
                            ARD2.objects.create(
                                jeton_commande=jeton,
                                debut_intervention=debut_intervention,
                                fin_intervention=fin_intervention,
                                terminee=terminee,
                                etat_intervention=etat if etat else "",
                                technicien=techniciens if techniciens else "",
                                departement=departement if departement else "",
                                pm=pm if pm else "",
                                date_importation=now,
                            )
                            self.stdout.write(self.style.SUCCESS(
                                f"🆕 Jeton {jeton} ajouté (date: {debut_intervention.date() if debut_intervention else 'N/A'})"
                            ))
                            imported_count += 1

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"❌ Erreur lors de l'importation pour la ligne : {row}"))
                        self.stdout.write(self.style.ERROR(str(e)))
                        skipped_count += 1

                self.stdout.write(self.style.SUCCESS(
                    f"\n✅ Import terminé. {imported_count} enregistrements traités, {skipped_count} ignorés."
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR("❌ Erreur lors de l'ouverture du fichier CSV."))
            self.stdout.write(self.style.ERROR(str(e)))

    def parse_date(self, date_str):
        for fmt in ["%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"]:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return make_aware(parsed_date)
            except Exception:
                continue
        return None
