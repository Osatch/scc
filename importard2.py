import csv
import os
import django
from django.utils import timezone

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import ARD2

def import_csv_to_ard2(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertir les dates
            debut_intervention = timezone.datetime.strptime(row['debut_intervention'], '%Y-%m-%d %H:%M:%S')
            fin_intervention = timezone.datetime.strptime(row['fin_intervention'], '%Y-%m-%d %H:%M:%S') if row['fin_intervention'] else None

            # Créer l'objet ARD2
            ARD2.objects.create(
                jeton_commande=row['jeton_commande'],
                debut_intervention=debut_intervention,
                fin_intervention=fin_intervention,
                etat_intervention=row['etat_intervention'],
                technicien=row['technicien'],
                departement=row['departement'],
                pm=row['pm']
            )
            print(f"Inserted: {row['jeton_commande']}")

if __name__ == "__main__":
    csv_file_path = 'ard2.csv'  # Remplacez par le chemin de votre fichier CSV
    import_csv_to_ard2(csv_file_path)