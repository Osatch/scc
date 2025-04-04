import csv
import os
import glob
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from django.db.models.signals import post_save
from core.models import GRDV, ARD2
from core.signals import create_or_update_relancejj_from_grdv, create_or_update_relancejj_from_ard2

class Command(BaseCommand):
    help = "Importe le dernier fichier CSV GRDV téléchargé dans la base de données sans déclencher la synchronisation RelanceJJ."

    def handle(self, *args, **options):
        # Déconnexion temporaire des signaux de synchronisation
        post_save.disconnect(create_or_update_relancejj_from_grdv, sender=GRDV)
        post_save.disconnect(create_or_update_relancejj_from_ard2, sender=ARD2)

        # Dossier contenant les fichiers CSV
        download_dir = os.path.join("Bot", "grdv")
        csv_pattern = os.path.join(download_dir, "*.csv")
        csv_files = glob.glob(csv_pattern)
        if not csv_files:
            self.stdout.write(self.style.ERROR(f"Aucun fichier CSV trouvé dans le dossier {download_dir}."))
            return

        # Sélection du fichier CSV le plus récent (basé sur la date de création)
        latest_file = max(csv_files, key=os.path.getctime)
        self.stdout.write(self.style.WARNING(f"Fichier CSV le plus récent détecté : {latest_file}"))

        try:
            with open(latest_file, mode='r', newline='', encoding='cp1252') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                date_format = "%Y-%m-%d %H:%M:%S"  # Format attendu dans le CSV

                for row in reader:
                    row = {k.strip(): v.strip() for k, v in row.items() if k is not None}

                    if not row.get('date_rdv'):
                        self.stdout.write(self.style.ERROR(f"Ligne ignorée (date_rdv vide) : {row}"))
                        continue

                    try:
                        # Conversion avec timezone
                        date_rdv = make_aware(datetime.strptime(row['date_rdv'], date_format)) if row.get('date_rdv') else None
                        debut = make_aware(datetime.strptime(row['debut'], date_format)) if row.get('debut') else None
                        fin = make_aware(datetime.strptime(row['fin'], date_format)) if row.get('fin') else None

                        secteur = row.get('secteur', '')
                        infra = row.get('infra', '')
                        secteur_infra = f"{secteur} {infra}".strip()

                        grdv = GRDV(
                            date_rdv=date_rdv,
                            debut=debut,
                            fin=fin,
                            statut_rendez_vous=row.get('statut_rendez-vous', ''),
                            statut_grdv=row.get('statut_grdv', ''),
                            activite=row.get('activite', ''),
                            plp=row.get('plp', ''),
                            technicien=row.get('technicien', ''),
                            presta=row.get('presta', ''),
                            tel_contact=row.get('tel_contact', ''),
                            commentaire=row.get('commentaire', ''),
                            adresse_postale=row.get('adresse_postale', ''),
                            ref_commande=row.get('ref_commande', ''),
                            nro=row.get('nro', ''),
                            pm=row.get('pm', ''),
                            code=row.get('code', ''),
                            residence=row.get('residence', ''),
                            bat=row.get('bat', ''),
                            esc=row.get('esc', ''),
                            eta=row.get('eta', ''),
                            por=row.get('por', ''),
                            pto=row.get('pto', ''),
                            id_client=row.get('id_client', ''),
                            technologement=row.get('technologement', ''),
                            operateurlogement=row.get('operateurlogement', ''),
                            typezone=row.get('typezone', ''),
                            typetechno=row.get('typetechno', ''),
                            secteur_infra=secteur_infra,
                            typebatiment=row.get('typebatiment', ''),
                            typepoteau_edf=row.get('typepoteau_edf', ''),
                            typeclient=row.get('typeclient', ''),
                            typebox=row.get('typebox', ''),
                            id_debrief_rdv=row.get('id_debrief_rdv', ''),
                            debrief_rdv=row.get('debrief_rdv', ''),
                            Adresse_PM=row.get('Adresse_PM', ''),
                            Connecteur_Free_PM=row.get('Connecteur_Free_PM', '')
                        )
                        grdv.save()

                    except Exception as row_error:
                        self.stdout.write(self.style.ERROR(f"Erreur lors du traitement de la ligne : {row}"))
                        self.stdout.write(self.style.ERROR(str(row_error)))
                        continue

            self.stdout.write(self.style.SUCCESS("✅ Importation du CSV GRDV terminée avec succès."))
        except Exception as e:
            self.stdout.write(self.style.ERROR("❌ Une erreur est survenue lors de l'importation du CSV."))
            self.stdout.write(self.style.ERROR(str(e)))
        finally:
            # Reconnexion des signaux après l'import
            post_save.connect(create_or_update_relancejj_from_grdv, sender=GRDV)
            post_save.connect(create_or_update_relancejj_from_ard2, sender=ARD2)
