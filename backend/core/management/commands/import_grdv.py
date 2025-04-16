from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from django.db.models.signals import post_save
from core.models import GRDV, ARD2
from core.signals import create_or_update_relancejj_from_grdv, create_or_update_relancejj_from_ard2

import os
import glob
import csv
from datetime import datetime

class Command(BaseCommand):
    help = "Import optimisé du dernier fichier CSV GRDV sans doublons."

    def handle(self, *args, **options):
        post_save.disconnect(create_or_update_relancejj_from_grdv, sender=GRDV)
        post_save.disconnect(create_or_update_relancejj_from_ard2, sender=ARD2)

        download_dir = os.path.join("Bot", "grdv")
        csv_pattern = os.path.join(download_dir, "*.csv")
        csv_files = glob.glob(csv_pattern)
        if not csv_files:
            self.stdout.write(self.style.ERROR(f"Aucun fichier CSV trouvé dans le dossier {download_dir}."))
            return

        latest_file = max(csv_files, key=os.path.getctime)
        self.stdout.write(self.style.WARNING(f"Fichier CSV détecté : {latest_file}"))

        with open(latest_file, 'rb') as rawfile:
            signature = rawfile.read(4)
        encoding = 'utf-8-sig' if signature.startswith(b'\xef\xbb\xbf') else 'cp1252'

        total_lignes = 0
        lignes_preparees = 0
        lignes_ignorees = 0
        lignes_en_erreur = 0
        objets_a_inserer = []

        # Récupération des clés uniques déjà en base
        existing_keys = set(
            GRDV.objects.values_list("ref_commande", "date_rdv").iterator()
        )

        date_format = "%Y-%m-%d %H:%M:%S"

        try:
            with open(latest_file, mode='r', encoding=encoding) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')

                for index, row in enumerate(reader, start=2):
                    total_lignes += 1
                    row = {k.strip(): v.strip() for k, v in row.items() if k}

                    if not any(row.values()) or not row.get("date_rdv"):
                        lignes_ignorees += 1
                        continue

                    try:
                        date_rdv = make_aware(datetime.strptime(row['date_rdv'], date_format))
                        debut = make_aware(datetime.strptime(row['debut'], date_format)) if row.get('debut') else None
                        fin = make_aware(datetime.strptime(row['fin'], date_format)) if row.get('fin') else None

                        cle = (row.get('ref_commande', ''), date_rdv)
                        if cle in existing_keys:
                            lignes_ignorees += 1
                            continue
                        existing_keys.add(cle)

                        secteur = row.get('secteur', '')
                        infra = row.get('infra', '')
                        secteur_infra = f"{secteur} {infra}".strip()

                        grdv = GRDV(
                            jeton=row.get('jeton', ''),
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
                        objets_a_inserer.append(grdv)
                        lignes_preparees += 1

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erreur ligne {index}: {e}"))
                        lignes_en_erreur += 1
                        continue

            # Insertion en une seule requête
            GRDV.objects.bulk_create(objets_a_inserer, batch_size=1000)

            # Résumé
            self.stdout.write(self.style.SUCCESS("✅ Import terminé."))
            self.stdout.write(self.style.SUCCESS(f"📄 Total lignes lues : {total_lignes}"))
            self.stdout.write(self.style.SUCCESS(f"✅ Lignes insérées : {lignes_preparees}"))
            self.stdout.write(self.style.WARNING(f"➖ Ignorées (doublons/vides) : {lignes_ignorees}"))
            self.stdout.write(self.style.ERROR(f"❌ Lignes en erreur : {lignes_en_erreur}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR("❌ Erreur globale :"))
            self.stdout.write(self.style.ERROR(str(e)))

        finally:
            post_save.connect(create_or_update_relancejj_from_grdv, sender=GRDV)
            post_save.connect(create_or_update_relancejj_from_ard2, sender=ARD2)
