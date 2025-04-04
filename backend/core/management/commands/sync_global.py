import csv
import os
import glob
import unicodedata
from datetime import datetime, time
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.timezone import make_aware
from core.models import (
    GRDV, ARD2, RelanceJJ, Parametres, Gantt, 
    ControlPhoto, DebriefRACC, DebriefSAV
)
from core.signals import create_or_update_relancejj_from_grdv, create_or_update_relancejj_from_ard2

class Command(BaseCommand):
    help = "Exécute toutes les synchronisations dans l'ordre requis"

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help="Date des interventions au format YYYY-MM-DD (par défaut aujourd'hui)"
        )

    def handle(self, *args, **options):
        # 1. Import GRDV
        self.stdout.write(self.style.NOTICE("Début de l'import GRDV..."))
        self.import_grdv()
        
        # 2. Import ARD2
        self.stdout.write(self.style.NOTICE("Début de l'import ARD2..."))
        self.import_ard2()
        
        # 3. Import Parametres
        self.stdout.write(self.style.NOTICE("Début de l'import Parametres..."))
        self.import_parametres()
        
        # 4. Synchronisation RelanceJJ
        self.stdout.write(self.style.NOTICE("Début de la synchronisation RelanceJJ..."))
        self.sync_relancejj()
        
        # 5. Synchronisation Gantt
        self.stdout.write(self.style.NOTICE("Début de la synchronisation Gantt..."))
        self.sync_gantt()
        
        # 6. Synchronisation ControlPhoto
        self.stdout.write(self.style.NOTICE("Début de la synchronisation ControlPhoto..."))
        self.sync_control_photo()
        
        # 7. Synchronisation DebriefRACC
        self.stdout.write(self.style.NOTICE("Début de la synchronisation DebriefRACC..."))
        self.sync_debrief_racc()
        
        # 8. Synchronisation DebriefSAV
        self.stdout.write(self.style.NOTICE("Début de la synchronisation DebriefSAV..."))
        self.sync_debrief_sav()
        
        self.stdout.write(self.style.SUCCESS("Toutes les synchronisations ont été exécutées avec succès."))

    def import_grdv(self):
        """Importe le dernier fichier CSV GRDV"""
        # Déconnexion temporaire des signaux de synchronisation
        post_save.disconnect(create_or_update_relancejj_from_grdv, sender=GRDV)
        post_save.disconnect(create_or_update_relancejj_from_ard2, sender=ARD2)

        try:
            # Dossier contenant les fichiers CSV
            download_dir = os.path.join("Bot", "grdv")
            csv_pattern = os.path.join(download_dir, "*.csv")
            csv_files = glob.glob(csv_pattern)
            if not csv_files:
                self.stdout.write(self.style.ERROR(f"Aucun fichier CSV trouvé dans le dossier {download_dir}."))
                return

            # Sélection du fichier CSV le plus récent
            latest_file = max(csv_files, key=os.path.getctime)
            self.stdout.write(self.style.WARNING(f"Fichier CSV le plus récent détecté : {latest_file}"))

            with open(latest_file, mode='r', newline='', encoding='cp1252') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                date_format = "%Y-%m-%d %H:%M:%S"

                for row in reader:
                    row = {k.strip(): v.strip() for k, v in row.items() if k is not None}

                    if not row.get('date_rdv'):
                        self.stdout.write(self.style.ERROR(f"Ligne ignorée (date_rdv vide) : {row}"))
                        continue

                    try:
                        date_rdv = datetime.strptime(row['date_rdv'], date_format) if row.get('date_rdv') else None
                        debut = datetime.strptime(row['debut'], date_format) if row.get('debut') else None
                        fin = datetime.strptime(row['fin'], date_format) if row.get('fin') else None

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

            self.stdout.write(self.style.SUCCESS("Importation du CSV GRDV terminée avec succès."))
        except Exception as e:
            self.stdout.write(self.style.ERROR("Une erreur est survenue lors de l'importation du CSV GRDV."))
            self.stdout.write(self.style.ERROR(str(e)))
        finally:
            # Reconnexion des signaux après l'import
            post_save.connect(create_or_update_relancejj_from_grdv, sender=GRDV)
            post_save.connect(create_or_update_relancejj_from_ard2, sender=ARD2)

    def import_ard2(self):
        """Importe le dernier fichier CSV ARD2"""
        csv_dir = os.path.join(settings.BASE_DIR, "Bot", "ard2")
        csv_pattern = os.path.join(csv_dir, "*.csv")
        
        csv_files = glob.glob(csv_pattern)
        if not csv_files:
            self.stdout.write(self.style.ERROR(f"Aucun fichier CSV trouvé dans {csv_dir}."))
            return
        
        latest_file = max(csv_files, key=os.path.getmtime)
        self.stdout.write(self.style.WARNING(f"Fichier CSV ARD2 détecté : {latest_file}"))

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
                        self.stdout.write(self.style.WARNING(f"Ligne ignorée (jeton vide) : {row}"))
                        skipped_count += 1
                        continue

                    debut_intervention = self.parse_date(debut_str) if debut_str else None
                    fin_intervention = self.parse_date(fin_str) if fin_str else None

                    if debut_str and debut_intervention is None:
                        self.stdout.write(self.style.ERROR(f"Erreur de conversion de la date pour la ligne : {row}"))
                        skipped_count += 1
                        continue

                    terminee = terminee_val.upper() == 'OUI' if terminee_val else False

                    try:
                        # Si debut_intervention est fourni, on compare la date uniquement.
                        if debut_intervention:
                            existing_entry = ARD2.objects.filter(
                                jeton_commande=jeton,
                                debut_intervention__date=debut_intervention.date()
                            ).first()
                        else:
                            existing_entry = ARD2.objects.filter(jeton_commande=jeton).first()

                        if existing_entry:
                            # Mise à jour des champs de l'entrée existante.
                            existing_entry.debut_intervention = debut_intervention
                            existing_entry.fin_intervention = fin_intervention
                            existing_entry.terminee = terminee
                            existing_entry.etat_intervention = etat if etat else ""
                            existing_entry.technicien = techniciens if techniciens else ""
                            existing_entry.departement = departement if departement else ""
                            existing_entry.pm = pm if pm else ""
                            existing_entry.date_importation = now
                            existing_entry.save()
                            self.stdout.write(self.style.SUCCESS(f"Jeton {jeton} mis à jour (date: {debut_intervention.date() if debut_intervention else 'N/A'})."))
                        else:
                            # Création d'une nouvelle entrée.
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
                            self.stdout.write(self.style.SUCCESS(f"Jeton {jeton} ajouté (date: {debut_intervention.date() if debut_intervention else 'N/A'})."))
                        imported_count += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erreur lors de l'importation pour la ligne : {row}"))
                        self.stdout.write(self.style.ERROR(str(e)))
                        skipped_count += 1

                self.stdout.write(self.style.SUCCESS(f"Import ARD2 terminé. {imported_count} enregistrements traités, {skipped_count} ignorés."))
        except Exception as e:
            self.stdout.write(self.style.ERROR("Erreur lors de l'importation du fichier CSV ARD2."))
            self.stdout.write(self.style.ERROR(str(e)))

    def import_parametres(self):
        """Importe le dernier fichier CSV Parametres"""
        folder_path = r"C:\scc\backend\Bot\param"
        csv_pattern = os.path.join(folder_path, "*.csv")
        csv_files = glob.glob(csv_pattern)

        if not csv_files:
            self.stdout.write(self.style.ERROR(f"Aucun fichier CSV trouvé dans le dossier {folder_path}."))
            return

        latest_file = max(csv_files, key=os.path.getctime)
        self.stdout.write(self.style.WARNING(f"Fichier CSV Parametres le plus récent détecté : {latest_file}"))

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
                    # Nouveaux champs ajoutés
                    nom_prenom_grdv = row.get('Nom prénom Grdv', '').strip() or '-'
                    id_grdv = row.get('ID Grdv', '').strip() or '-'
                    
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
                        'nom_prenom_grdv': nom_prenom_grdv,
                        'id_grdv': id_grdv,
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
                            existing.societe == societe and
                            existing.nom_prenom_grdv == nom_prenom_grdv and
                            existing.id_grdv == id_grdv
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
                    f"Import Parametres terminé. {imported_count} enregistrements traités."
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR("Une erreur est survenue lors de l'import du CSV Parametres."))
            self.stdout.write(self.style.ERROR(str(e)))

    def sync_relancejj(self):
        """Synchronise les données de GRDV et ARD2 dans RelanceJJ"""
        # Affichage des valeurs de jeton_commande présentes dans ARD2 pour débogage
        ard2_values = list(ARD2.objects.values_list('jeton_commande', flat=True))
        self.stdout.write(self.style.NOTICE(f"Nombre total d'ARD2 : {len(ard2_values)}"))
        self.stdout.write(self.style.NOTICE(f"Exemple de valeurs ARD2 : {ard2_values[:10]}"))

        for grdv in GRDV.objects.all():
            if not grdv.ref_commande:
                self.stdout.write(self.style.WARNING(
                    f"GRDV {grdv.id} n'a pas de ref_commande définie, passage au suivant."
                ))
                continue

            # Affichage de la valeur brute pour débogage
            self.stdout.write(self.style.NOTICE(
                f"Valeur brute ref_commande pour GRDV {grdv.id} : {repr(grdv.ref_commande)}"
            ))
            
            # Normalisation de ref_commande
            ref_norm = unicodedata.normalize("NFKC", grdv.ref_commande.strip())[:10]
            self.stdout.write(f"Recherche pour GRDV {grdv.id} avec ref_commande normalisé = '{ref_norm}'")

            # Recherche de l'instance ARD2 correspondante (insensible à la casse)
            ard2_instance = ARD2.objects.filter(jeton_commande__iexact=ref_norm).first()
            if not ard2_instance:
                self.stdout.write(self.style.WARNING(
                    f"GRDV {grdv.id} n'a pas d'ARD2 associé (ref_commande: {ref_norm}), passage au suivant."
                ))
                continue

            # Détermination de la date du RDV à partir de GRDV (si elle existe)
            date_rdv = grdv.date_rdv.date() if grdv.date_rdv else None

            # Préparation des valeurs à mettre à jour/créer dans RelanceJJ
            defaults = {
                "grdv": grdv,  # Association à GRDV
                "heure_debut": ard2_instance.debut_intervention.time() if ard2_instance.debut_intervention else None,
                "heure_fin": ard2_instance.fin_intervention.time() if ard2_instance.fin_intervention else None,
                "departement": ard2_instance.departement if ard2_instance.departement else None,
                "techniciens": ard2_instance.technicien  # Affecte techniciens de RelanceJJ avec technicien de ARD2
            }

            # Recherche dans RelanceJJ avec jeton_commande ET date_rdv
            relance_qs = RelanceJJ.objects.filter(
                jeton_commande=ard2_instance.jeton_commande,
                date_rdv=date_rdv
            )

            if relance_qs.exists():
                # Si une entrée correspondante existe, on la met à jour
                relance = relance_qs.first()
                for key, value in defaults.items():
                    setattr(relance, key, value)
                relance.save()
                action = "Mis à jour"
            else:
                # Sinon, on crée une nouvelle entrée
                defaults.update({
                    "jeton_commande": ard2_instance.jeton_commande
                })
                relance = RelanceJJ.objects.create(**defaults)
                action = "Créé"

            self.stdout.write(self.style.SUCCESS(f"{action} RelanceJJ pour GRDV {grdv.id} (date_rdv: {date_rdv})"))

            # Synchronisation du numéro technicien et de la société à partir de la table Parametres.
            param = Parametres.objects.filter(
                nom_tech__iexact=relance.techniciens,
                departement__iexact=relance.departement
            ).first()

            if param:
                if param.numero_technicien:
                    relance.numero = param.numero_technicien
                if param.societe:
                    relance.societe = param.societe
                relance.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Mis à jour le numéro technicien et la société pour RelanceJJ de GRDV {grdv.id} (numéro: {param.numero_technicien}, société: {param.societe})"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Aucun paramètre trouvé pour technicien '{relance.techniciens}' et département '{relance.departement}' pour GRDV {grdv.id}"
                ))

    def sync_gantt(self, date_str=None):
        """Importe les interventions dans Gantt pour une journée donnée"""
        # Détermination de la date à traiter
        if date_str:
            try:
                intervention_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR("Format de date invalide. Utilisez YYYY-MM-DD."))
                return
        else:
            intervention_date = timezone.localdate()

        self.stdout.write(self.style.NOTICE(f"Début de l'importation dans Gantt pour le {intervention_date}..."))

        # Récupérer les interventions de la journée (ARD2) dont le champ debut_intervention est défini
        ard2_qs = ARD2.objects.filter(debut_intervention__date=intervention_date)
        if not ard2_qs.exists():
            self.stdout.write(self.style.WARNING(f"Aucune intervention trouvée pour le {intervention_date}."))
            return

        # Regrouper les données par technicien
        gantt_data = {}
        for ard in ard2_qs:
            # On ignore les interventions sans heure de début
            if not ard.debut_intervention:
                continue

            # Récupérer l'enregistrement RelanceJJ associé à cette intervention, si disponible
            relance = RelanceJJ.objects.filter(jeton_commande=ard.jeton_commande).first()

            # Déterminer le créneau horaire en fonction de l'heure de début
            hour = ard.debut_intervention.hour
            if 8 <= hour <= 15:
                slot = f"heure_{hour:02d}"
                base_status = ard.etat_intervention.upper() if ard.etat_intervention else ""
                if relance:
                    activite = getattr(relance, "activite", "")
                    activite = activite.upper() if activite else ""
                    statut = getattr(relance, "statut", "")
                    statut = statut.lower() if statut else ""
                    status_str = f"{base_status} {activite}".strip()
                    if statut == "taguée":
                        status_str += " EN COURS"
                else:
                    status_str = base_status
            elif hour in [16, 17] or hour >= 18:
                slot = "heure_18" if hour >= 18 else f"heure_{hour:02d}"
                status_str = ard.etat_intervention.upper() if ard.etat_intervention else ""
            else:
                continue

            technicien = ard.technicien
            # Initialiser les données pour ce technicien pour ce jour
            if technicien not in gantt_data:
                gantt_data[technicien] = {
                    "secteur": ard.departement,          # Conserve secteur/département si besoin
                    "departement": ard.departement,
                    "nom_intervenant": technicien,
                    "heure_08": "",
                    "heure_09": "",
                    "heure_10": "",
                    "heure_11": "",
                    "heure_12": "",
                    "heure_13": "",
                    "heure_14": "",
                    "heure_15": "",
                    "heure_16": "",
                    "heure_17": "",
                    "heure_18": "",
                    "interventions": {}
                }
            # Concaténer les interventions dans le même créneau si nécessaire (séparées par "; ")
            current_val = gantt_data[technicien]["interventions"].get(slot, "")
            new_val = current_val + "; " + status_str if current_val else status_str
            gantt_data[technicien]["interventions"][slot] = new_val

        # Mise à jour / création des enregistrements Gantt
        with transaction.atomic():
            for technicien, data in gantt_data.items():
                horaires = {
                    "heure_08": data["interventions"].get("heure_08", ""),
                    "heure_09": data["interventions"].get("heure_09", ""),
                    "heure_10": data["interventions"].get("heure_10", ""),
                    "heure_11": data["interventions"].get("heure_11", ""),
                    "heure_12": data["interventions"].get("heure_12", ""),
                    "heure_13": data["interventions"].get("heure_13", ""),
                    "heure_14": data["interventions"].get("heure_14", ""),
                    "heure_15": data["interventions"].get("heure_15", ""),
                    "heure_16": data["interventions"].get("heure_16", ""),
                    "heure_17": data["interventions"].get("heure_17", ""),
                    "heure_18": data["interventions"].get("heure_18", ""),
                }

                # Calcul des indicateurs
                ok_count = 0
                filled_cells = 0
                for val in horaires.values():
                    if val:
                        filled_cells += 1
                        if val.upper().startswith("OK"):
                            ok_count += 1
                taux_transfo = (ok_count / filled_cells * 100) if filled_cells > 0 else 0

                total_slots = 11
                filled_total = sum(1 for v in horaires.values() if v)
                taux_remplissage = (filled_total / total_slots * 100)

                # Ici, update_or_create utilise nom_intervenant et date_intervention pour éviter les doublons
                gantt_obj, created = Gantt.objects.update_or_create(
                    nom_intervenant=data["nom_intervenant"],
                    date_intervention=intervention_date,
                    defaults={
                        "secteur": data["secteur"],
                        "departement": data["departement"],
                        "heure_08": horaires["heure_08"],
                        "heure_09": horaires["heure_09"],
                        "heure_10": horaires["heure_10"],
                        "heure_11": horaires["heure_11"],
                        "heure_12": horaires["heure_12"],
                        "heure_13": horaires["heure_13"],
                        "heure_14": horaires["heure_14"],
                        "heure_15": horaires["heure_15"],
                        "heure_16": horaires["heure_16"],
                        "heure_17": horaires["heure_17"],
                        "heure_18": horaires["heure_18"],
                        "taux_transfo": taux_transfo,
                        "taux_remplissage": taux_remplissage,
                    }
                )
                action = "Créé" if created else "Mis à jour"
                self.stdout.write(self.style.SUCCESS(f"{action} Gantt pour {data['nom_intervenant']} - {intervention_date}"))

        self.stdout.write(self.style.SUCCESS("Importation Gantt terminée."))

    def sync_control_photo(self):
        """Synchronise les données de RelanceJJ dans ControlPhoto"""
        relances = RelanceJJ.objects.all()
        self.stdout.write(self.style.NOTICE(f"Nombre total de RelanceJJ : {relances.count()}"))

        for relance in relances:
            # Préparation des valeurs à mettre à jour/créer dans ControlPhoto
            defaults = {
                "jeton": relance.jeton_commande,  # Ajout direct du champ jeton
                "date": relance.date_rdv,
                "heure": relance.heure_prevue,
                "tech": relance.techniciens,
                "numero": relance.numero,
                "groupe_tech": "G1",              # Valeur par défaut (ajustez si nécessaire)
                "actif_depuis": relance.date_rdv,   # Utilise date_rdv comme date d'activité par défaut
                "zone_manager": "#N/A",           # Valeur par défaut
                "statut": relance.statut,
                "secteur": relance.departement,
                "societe": relance.societe,
            }

            # Récupération de l'instance ARD2 liée via jeton_commande
            ard_instance = ARD2.objects.filter(jeton_commande=relance.jeton_commande).first()
            if ard_instance:
                defaults["synchro"] = ard_instance.etat_intervention
            else:
                defaults["synchro"] = None  # ou définir une valeur par défaut

            # Recherche d'une instance ControlPhoto liée à ce RelanceJJ via jeton
            control_photo_instance = ControlPhoto.objects.filter(jeton=relance.jeton_commande).first()

            if control_photo_instance:
                # Mise à jour de l'instance existante
                for key, value in defaults.items():
                    setattr(control_photo_instance, key, value)
                control_photo_instance.save()
                action = "Mis à jour"
            else:
                # Création d'une nouvelle instance avec les valeurs par défaut
                control_photo_instance = ControlPhoto.objects.create(**defaults)
                action = "Créé"

            self.stdout.write(self.style.SUCCESS(
                f"{action} ControlPhoto pour RelanceJJ avec jeton {relance.jeton_commande}"
            ))

    def sync_debrief_racc(self):
        """Synchronise les données dans DebriefRACC"""
        relances = RelanceJJ.objects.filter(activite="RACC")
        self.stdout.write(self.style.NOTICE(f"Relances RACC détectées : {relances.count()}"))

        compteur = 0

        for relance in relances:
            # Vérifie que ARD2 associé existe et est NOK
            ard2 = ARD2.objects.filter(jeton_commande=relance.jeton_commande, etat_intervention="NOK").first()
            if not ard2:
                continue

            # Control à froid (ControlPhoto) pour appel_tech & resultat_controle
            control_photo = ControlPhoto.objects.filter(jeton=relance.jeton_commande).first()

            # Parametres pour numéro technicien et manager
            parametre = Parametres.objects.filter(numero_technicien=relance.numero).first()

            # Calcul du champ synchro selon conditions combinées
            if relance.statut == "Cloturée" and ard2.etat_intervention == "NOK":
                synchro_value = "Echec"
            elif relance.statut == "Taguée":
                synchro_value = "Taguées"
            else:
                synchro_value = ""

            # Préparation des données à injecter
            defaults = {
                "jeton": relance.jeton_commande,
                "date": relance.date_rdv,
                "tech": relance.techniciens,
                "numero_technicien": relance.numero,
                "secteur": relance.departement,
                "zone_manager": parametre.zone if parametre else None,
                "reference_pm": ard2.pm,
                "appel_tech": control_photo.statut_appel if control_photo else None,
                "synchro": synchro_value,
                "pec_par": control_photo.agent if control_photo else None,
                "resultat_controle": control_photo.resultats_verification if control_photo else None,
                "societe": relance.societe,
                "manager": parametre.manager if parametre else None,
                "nouveaux_tech": relance.techniciens,
                "code_cloture_technicien": "",
                "type_echec": "Echec client",  # Valeur par défaut, modifiable
                "diagnostic": "",
                "action": "",
            }

            # Création ou mise à jour de DebriefRACC
            instance, created = DebriefRACC.objects.update_or_create(
                jeton=relance.jeton_commande,
                defaults=defaults
            )

            compteur += 1
            self.stdout.write(self.style.SUCCESS(
                f"{'Créé' if created else 'Mis à jour'} : {relance.jeton_commande}"
            ))

        self.stdout.write(self.style.SUCCESS(f"Total DebriefRACC synchronisés : {compteur}"))

    def sync_debrief_sav(self):
        """Synchronise les données dans DebriefSAV"""
        relances = RelanceJJ.objects.filter(activite="RACC")
        self.stdout.write(self.style.NOTICE(f"Relances RACC détectées : {relances.count()}"))

        compteur = 0

        for relance in relances:
            # Ne traite que si ARD2 existe et NOK
            ard2 = ARD2.objects.filter(jeton_commande=relance.jeton_commande, etat_intervention="NOK").first()
            if not ard2:
                continue

            control_photo = ControlPhoto.objects.filter(jeton=relance.jeton_commande).first()
            parametre = Parametres.objects.filter(numero_technicien=relance.numero).first()
            grdv = relance.grdv

            # Détermine la valeur de synchronisation
            if relance.statut == "Cloturée" and ard2.etat_intervention == "NOK":
                synchro_value = "Echec"
            elif relance.statut == "Taguée":
                synchro_value = "Taguée"
            elif relance.statut == "Cloturée" and ard2.etat_intervention == "OK":
                synchro_value = "OK"
            else:
                synchro_value = ""

            defaults = {
                "date": relance.date_rdv,
                "heure": relance.heure_prevue,
                "tech": relance.techniciens,
                "numero_tech": relance.numero,
                "secteur": relance.departement,
                "zone_manager": parametre.zone if parametre else None,
                "reference_pm": ard2.pm if ard2 else None,
                "appel_tech": control_photo.statut_appel if control_photo else None,
                "synchro": synchro_value,
                "pec_par": control_photo.agent if control_photo else None,
                "resultat_controle": control_photo.resultats_verification if control_photo else None,
                "societe": relance.societe,
                "manager": parametre.manager if parametre else None,
                "tel_contact": grdv.tel_contact if grdv else None,
            }

            instance, created = DebriefSAV.objects.update_or_create(
                jeton=relance,
                defaults=defaults
            )

            compteur += 1
            self.stdout.write(self.style.SUCCESS(
                f"{'Créé' if created else 'Mis à jour'} : {relance.jeton_commande}"
            ))

        self.stdout.write(self.style.SUCCESS(f"Total DebriefSAV synchronisés : {compteur}"))

    def parse_date(self, date_str):
        """Helper method to parse date strings"""
        for fmt in ["%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"]:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return make_aware(parsed_date)
            except Exception:
                continue
        return None