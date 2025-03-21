import csv
import os
import glob
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from core.models import ARD2

class Command(BaseCommand):
    help = "Importe le dernier fichier CSV ARD2 téléchargé dans la base de données."

    def handle(self, *args, **options):
        # Chemin absolu vers le dossier CSV, par exemple: C:\scc\backend\Bot\ard2
        csv_dir = os.path.join(settings.BASE_DIR, "Bot", "ard2")
        csv_pattern = os.path.join(csv_dir, "*.csv")
        
        csv_files = glob.glob(csv_pattern)
        if not csv_files:
            self.stdout.write(self.style.ERROR(f"Aucun fichier CSV trouvé dans {csv_dir}."))
            return
        
        # Sélectionner le fichier le plus récent (basé sur la date de modification)
        latest_file = max(csv_files, key=os.path.getmtime)
        self.stdout.write(self.style.WARNING(f"Fichier CSV détecté : {latest_file}"))

        try:
            # Utiliser 'utf-8-sig' pour gérer le BOM et ';' comme séparateur
            with open(latest_file, mode='r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                # Format de date mis à jour (avec secondes)
                date_format = "%d/%m/%Y %H:%M:%S"

                imported_count = 0
                skipped_count = 0

                for row in reader:
                    # Normaliser les clés en minuscules et retirer les espaces superflus
                    row = {k.strip().lower(): v.strip() for k, v in row.items() if k is not None}

                    # >>> CHANGEMENT PRINCIPAL <<<
                    # Au lieu de récupérer row.get('référence'), on récupère la colonne "jeton de commande"
                    # qui, une fois en minuscules, s'appelle "jeton de commande".
                    jeton = row.get('jeton de commande')

                    debut_str = row.get("début d'intervention")
                    fin_str = row.get("fin d'intervention")
                    terminee_val = row.get("terminée")
                    etat = row.get("état de l'intervention")
                    techniciens = row.get("techniciens")
                    departement = row.get("département")
                    pm = row.get("pm")

                    # Vérifier que le champ 'jeton de commande' est présent (champ obligatoire)
                    if not jeton:
                        self.stdout.write(
                            self.style.WARNING(f"Ligne ignorée (champ 'jeton de commande' vide) : {row}")
                        )
                        skipped_count += 1
                        continue

                    # Conversion des dates : si le champ est vide, on met None
                    debut_intervention = self.parse_date(debut_str, date_format) if debut_str else None
                    fin_intervention = self.parse_date(fin_str, date_format) if fin_str else None

                    # Optionnel : si le champ de date est présent mais mal converti, on ignore la ligne
                    if debut_str and debut_intervention is None:
                        self.stdout.write(self.style.ERROR(
                            f"Erreur de conversion de la date 'Début d'intervention' pour la ligne : {row}"
                        ))
                        skipped_count += 1
                        continue

                    terminee = False
                    if terminee_val:
                        terminee = terminee_val.upper() == 'OUI'

                    try:
                        obj, created = ARD2.objects.update_or_create(
                            jeton_commande=jeton,
                            defaults={
                                'debut_intervention': debut_intervention,
                                'fin_intervention': fin_intervention,
                                'terminee': terminee,
                                'etat_intervention': etat if etat else "",
                                'technicien': techniciens if techniciens else "",
                                'departement': departement if departement else "",
                                'pm': pm if pm else "",
                                'date_importation': make_aware(datetime.now()),
                            }
                        )
                        imported_count += 1
                        action = "créé" if created else "mis à jour"
                        self.stdout.write(self.style.SUCCESS(f"ARD2 {action} pour le jeton {jeton}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erreur lors de l'importation de la ligne : {row}"))
                        self.stdout.write(self.style.ERROR(str(e)))
                        skipped_count += 1

                self.stdout.write(self.style.SUCCESS(
                    f"Importation terminée. Lignes importées: {imported_count}, Lignes ignorées: {skipped_count}"
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR("Une erreur est survenue lors de l'importation du CSV."))
            self.stdout.write(self.style.ERROR(str(e)))

    def parse_date(self, date_str, date_format):
        if not date_str or date_str.strip() == '':
            return None
        try:
            parsed_date = datetime.strptime(date_str, date_format)
            return make_aware(parsed_date)
        except Exception:
            return None
