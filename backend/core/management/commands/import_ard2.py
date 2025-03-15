import csv
import os
import glob
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from core.models import ARD2  # Vérifiez que le chemin correspond bien à votre modèle ARD2

class Command(BaseCommand):
    help = "Importe le dernier fichier CSV ARD2 téléchargé dans la base de données."

    def handle(self, *args, **options):
        # 1. Chemin vers le dossier contenant les CSV (relatif à la racine du projet)
        csv_dir = os.path.join("Bot", "ard2")
        csv_pattern = os.path.join(csv_dir, "*.csv")

        # 2. Récupérer tous les fichiers CSV dans le dossier
        csv_files = glob.glob(csv_pattern)
        if not csv_files:
            self.stdout.write(self.style.ERROR(f"Aucun fichier CSV trouvé dans {csv_dir}."))
            return

        # 3. Sélectionner le fichier CSV le plus récent (basé sur la date de création)
        latest_file = max(csv_files, key=os.path.getctime)
        self.stdout.write(self.style.WARNING(f"Fichier CSV détecté : {latest_file}"))

        try:
            # 4. Ouvrir le fichier CSV
            # Assurez-vous que l'encodage et le délimiteur correspondent à votre fichier ard2.csv.
            # Ici, nous utilisons UTF-8 et la tabulation ('\t') comme séparateur.
            with open(latest_file, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='\t')
                date_format = "%d/%m/%Y %H:%M"  # Par exemple "25/02/2025 09:34"

                for row in reader:
                    # Nettoyer les clés et valeurs pour retirer les espaces superflus
                    row = {k.strip(): v.strip() for k, v in row.items() if k is not None}

                    # Vérifier que les champs obligatoires sont présents
                    if not row.get('Jeton de commande') or not row.get("Début d'intervention"):
                        self.stdout.write(self.style.WARNING(f"Ligne ignorée (champ requis vide) : {row}"))
                        continue

                    # Conversion des dates
                    debut_intervention = self.parse_date(row.get("Début d'intervention"), date_format)
                    fin_intervention = self.parse_date(row.get("Fin d'intervention"), date_format)

                    try:
                        ARD2.objects.update_or_create(
                            jeton_commande=row['Jeton de commande'],
                            defaults={
                                'debut_intervention': debut_intervention,
                                'fin_intervention': fin_intervention,
                                'terminee': row['Terminée'].upper() == 'OUI',
                                'etat_intervention': row["État de l'intervention"],
                                'technicien': row['Techniciens'],
                                'departement': row['Département'],
                                'pm': row['PM'],
                                'date_importation': make_aware(datetime.now()),
                            }
                        )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erreur lors de l'importation de la ligne : {row}"))
                        self.stdout.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.SUCCESS("Importation terminée avec succès."))

        except Exception as e:
            self.stdout.write(self.style.ERROR("Une erreur est survenue lors de l'importation du CSV."))
            self.stdout.write(self.style.ERROR(str(e)))

    def parse_date(self, date_str, date_format):
        if not date_str or date_str.strip() == '':
            return None
        try:
            return make_aware(datetime.strptime(date_str, date_format))
        except ValueError:
            return None
