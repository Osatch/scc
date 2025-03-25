import csv
import os
import glob
from datetime import datetime
from django.core.management.base import BaseCommand
from core.models import Parametres

class Command(BaseCommand):
    help = ("Importe le dernier fichier CSV trouvé dans le dossier "
            "C:\\scc\\backend\\Bot\\param dans la table Parametres, "
            "en remplaçant les valeurs vides par un tiret pour les champs texte, "
            "et en gérant le champ 'Actif depuis' vide en assignant la date du jour.")

    def handle(self, *args, **options):
        # Chemin absolu vers le dossier contenant le fichier CSV
        folder_path = r"C:\scc\backend\Bot\param"
        csv_pattern = os.path.join(folder_path, "*.csv")
        csv_files = glob.glob(csv_pattern)

        if not csv_files:
            self.stdout.write(self.style.ERROR(f"Aucun fichier CSV trouvé dans le dossier {folder_path}."))
            return

        # Sélection du fichier CSV le plus récent (basé sur la date de création)
        latest_file = max(csv_files, key=os.path.getctime)
        self.stdout.write(self.style.WARNING(f"Fichier CSV le plus récent détecté : {latest_file}"))

        try:
            with open(latest_file, mode='r', newline='', encoding='cp1252') as f:
                reader = csv.DictReader(f, delimiter=';')
                imported_count = 0

                for row in reader:
                    # Récupération et remplacement des valeurs vides par un tiret pour les champs texte
                    id_tech = row.get('ID tech', '').strip() or '-'
                    nom_tech = row.get('Tech', '').strip() or '-'
                    departement = row.get('Département', '').strip() or '-'
                    log_free = row.get('Log free', '').strip() or '-'
                    numero_technicien = row.get('Numéro', '').strip() or '-'
                    # Pour le champ date, on récupère la valeur brute
                    actif_depuis_str = row.get('Actif depuis', '').strip()
                    controle_photo = row.get('Controle photo', '').strip() or '-'
                    manager = row.get('Manager', '').strip() or '-'
                    zone = row.get('Zone', '').strip() or '-'
                    grille_actif = row.get('grille actif', '').strip() or '-'
                    societe = row.get('Nom de la sociètèe', '').strip() or '-'

                    # Gestion du champ "Actif depuis" (date)
                    if actif_depuis_str:
                        try:
                            actif_depuis = datetime.strptime(actif_depuis_str, "%d/%m/%Y").date()
                        except ValueError:
                            self.stdout.write(self.style.ERROR(
                                f"Format de date invalide pour 'Actif depuis' : {actif_depuis_str} (attendu: JJ/MM/AAAA)"
                            ))
                            continue
                    else:
                        actif_depuis = datetime.today().date()
                        self.stdout.write(self.style.NOTICE(
                            f"Champ 'Actif depuis' vide pour ID tech {id_tech}. Utilisation de la date du jour : {actif_depuis}."
                        ))

                    # Préparation du dictionnaire des valeurs à mettre à jour/créer
                    defaults = {
                        'nom_tech': nom_tech,
                        'departement': departement,
                        'log_free': log_free,
                        'numero_technicien': numero_technicien,
                        'actif_depuis': actif_depuis,
                        'controle_photo': controle_photo,
                        'manager': manager,
                        'zone': zone,
                        'grille_actif': grille_actif,
                        'societe': societe,
                    }

                    # Vérification pour éviter l'enregistrement des mêmes données
                    existing = Parametres.objects.filter(id_tech=id_tech).first()
                    if existing:
                        if (
                            existing.nom_tech == nom_tech and
                            existing.departement == departement and
                            existing.log_free == log_free and
                            existing.numero_technicien == numero_technicien and
                            existing.actif_depuis == actif_depuis and
                            existing.controle_photo == controle_photo and
                            existing.manager == manager and
                            existing.zone == zone and
                            existing.grille_actif == grille_actif and
                            existing.societe == societe
                        ):
                            self.stdout.write(self.style.NOTICE(
                                f"Enregistrement déjà existant et identique pour ID tech {id_tech}."
                            ))
                            continue
                        else:
                            # Mise à jour des champs si une différence est détectée
                            for key, value in defaults.items():
                                setattr(existing, key, value)
                            existing.save()
                            imported_count += 1
                            self.stdout.write(self.style.SUCCESS(
                                f"Mis à jour : {existing.id_tech} - {existing.nom_tech}"
                            ))
                    else:
                        # Création d'un nouvel enregistrement
                        parametre = Parametres.objects.create(id_tech=id_tech, **defaults)
                        imported_count += 1
                        self.stdout.write(self.style.SUCCESS(
                            f"Créé : {parametre.id_tech} - {parametre.nom_tech}"
                        ))

                self.stdout.write(self.style.SUCCESS(
                    f"Import terminé. {imported_count} enregistrements traités."
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR("Une erreur est survenue lors de l'import du CSV."))
            self.stdout.write(self.style.ERROR(str(e)))
