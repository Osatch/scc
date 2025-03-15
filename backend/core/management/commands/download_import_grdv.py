from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback
import os
import csv
import glob
from datetime import datetime
from django.core.management.base import BaseCommand
from core.models import GRDV

class Command(BaseCommand):
    help = "Télécharge le fichier CSV GRDV et l'importe dans la base de données."

    def handle(self, *args, **options):
        # Configuration pour le mode headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Exécuter en arrière-plan
        chrome_options.add_argument("--disable-gpu")  # Désactiver GPU pour éviter des erreurs
        chrome_options.add_argument("--window-size=1920x1080")  # Taille de la fenêtre
        chrome_options.add_argument("--disable-machine-learning")  # Désactiver TensorFlow Lite

        # Définir le dossier de téléchargement
        download_dir = r"C:\scc\backend\Bot\grdv"  # Dossier de téléchargement
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,  # Désactiver la boîte de dialogue de téléchargement
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Utiliser webdriver-manager pour gérer chromedriver
        service = Service(ChromeDriverManager().install())

        # Initialiser le navigateur en mode headless
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Dossier pour enregistrer les captures d'écran en cas d'erreur
        screenshot_dir = os.path.join(download_dir, "screenshots")
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        try:
            # Aller sur la page de login
            driver.get("https://grdv.proxad.net/grdv/cgi/index.pl?action=decon")
            time.sleep(2)  # Attendre que la page se charge

            # Remplir le champ login avec XPath
            login_field = driver.find_element(By.XPATH, '//*[@id="Lelogin"]')
            login_field.send_keys("TECHNO_SMART")

            # Remplir le champ mot de passe avec XPath
            password_field = driver.find_element(By.XPATH, '//*[@id="mdp"]')
            password_field.send_keys("BEJAtechno2025/")

            # Cliquer sur le bouton de validation avec XPath
            login_button = driver.find_element(By.XPATH, '//*[@id="valid_login"]')
            login_button.click()

            # Attendre que la page se charge après la connexion
            time.sleep(5)
            # Cliquer sur l'élément contenant le texte "Statistiques"
            second_menu_item = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Statistiques")]'))
            )
            print("Élément trouvé : Statistiques")
            second_menu_item.click()

            time.sleep(2)
            # Cliquer sur l'élément visible
            second_menu_item = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Vision Ressources")]'))
            )
            print("Élément trouvé : Vision Ressources")
            second_menu_item.click()
            time.sleep(2)

            # Attendre que l'élément <select> soit présent et cliquable (en utilisant XPath)
            select_element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="bt_select_exportbatch"]'))
            )
            print("Élément <select> trouvé et cliquable")

            # Sélectionner l'option souhaitée
            select = Select(select_element)
            target_option_text = "- Tout secteurs - Exporter les rdvs sur journée"
            select.select_by_visible_text(target_option_text)  # Sélectionner l'option par son texte visible
            print(f"Option sélectionnée : {target_option_text}")
            time.sleep(2)

            # Étape 4 : Cliquer sur une case à cocher
            checkbox = driver.find_element(By.XPATH, '//*[@id="jqgh_listeTech_cb"]')
            checkbox.click()
            time.sleep(2)

            download_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@type="button" and @value="Confirmer la sélection pour l\'export en mode CSV"]'))
            )
            download_button.click()
            time.sleep(5)  # Attendre que le téléchargement se termine

            # Cliquer sur le bouton contenant le texte "Lancer l'export en mode CSV"
            download_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Lancer l\'export en mode CSV")]'))
            )
            download_button.click()
            time.sleep(5)  # Attendre que le téléchargement se termine

            print(f"Téléchargement du fichier CSV terminé. Le fichier est enregistré dans : {download_dir}")

            # 1. Rechercher tous les fichiers CSV dans le dossier
            csv_pattern = os.path.join(download_dir, "*.csv")
            csv_files = glob.glob(csv_pattern)
            if not csv_files:
                self.stdout.write(self.style.ERROR(f"Aucun fichier CSV trouvé dans le dossier {download_dir}."))
                return

            # 2. Sélectionner le fichier CSV le plus récent (basé sur la date de création)
            latest_file = max(csv_files, key=os.path.getctime)
            self.stdout.write(self.style.WARNING(f"Fichier CSV le plus récent détecté : {latest_file}"))

            try:
                # 3. Ouvrir le fichier CSV avec l'encodage cp1252 et en précisant le délimiteur ';'
                with open(latest_file, mode='r', newline='', encoding='cp1252') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';')
                    # Format des dates dans le CSV (exemple : "2025-03-14 11:00:00")
                    date_format = "%Y-%m-%d %H:%M:%S"
                    
                    for row in reader:
                        # Nettoyer les clés et valeurs pour retirer les espaces superflus
                        row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                        
                        # Vérifier que le champ date_rdv est présent
                        if not row.get('date_rdv'):
                            self.stdout.write(self.style.ERROR(f"Ligne ignorée (date_rdv vide) : {row}"))
                            continue

                        try:
                            # Conversion des dates
                            date_rdv = datetime.strptime(row['date_rdv'], date_format) if row.get('date_rdv') else None
                            debut = datetime.strptime(row['debut'], date_format) if row.get('debut') else None
                            fin = datetime.strptime(row['fin'], date_format) if row.get('fin') else None

                            # Combiner les colonnes 'secteur' et 'infra' pour alimenter le champ secteur_infra
                            secteur = row.get('secteur', '')
                            infra = row.get('infra', '')
                            secteur_infra = f"{secteur} {infra}".strip()

                            # Créer l'instance GRDV en mappant les colonnes du CSV aux champs du modèle
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
                                pto=row.get('pto', '),
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

                self.stdout.write(self.style.SUCCESS("Importation du CSV terminée avec succès."))
            except Exception as e:
                self.stdout.write(self.style.ERROR("Une erreur est survenue lors de l'importation du CSV."))
                self.stdout.write(self.style.ERROR(str(e)))

        except Exception as e:
            # Capturer une capture d'écran en cas d'erreur
            screenshot_path = os.path.join(screenshot_dir, f"error_{int(time.time())}.png")
            driver.save_screenshot(screenshot_path)
            print(f"Capture d'écran sauvegardée : {screenshot_path}")

            # Afficher l'erreur
            print(f"Une erreur s'est produite : {e}")
            print(f"Traceback : {traceback.format_exc()}")  # Afficher la trace complète de l'erreur
        finally:
            # Fermer le navigateur
            driver.quit()