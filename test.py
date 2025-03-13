from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuration pour le mode headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # Exécuter en arrière-plan
chrome_options.add_argument("--disable-gpu")  # Désactiver GPU pour éviter des erreurs
chrome_options.add_argument("--window-size=1920x1080")  # Taille de la fenêtre

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

try:
    # Aller sur la page de login
    driver.get("https://grdv.proxad.net/grdv/cgi/index.pl?action=decon")  # Remplacez par l'URL de votre page de login
    time.sleep(2)  # Attendre que la page se charge

    # Remplir le champ login avec XPath
    login_field = driver.find_element(By.XPATH, '//*[@id="Lelogin"]')  # XPath du champ login
    login_field.send_keys("TECHNO_SMART")  # Remplacez par votre nom d'utilisateur

    # Remplir le champ mot de passe avec XPath
    password_field = driver.find_element(By.XPATH, '//*[@id="mdp"]')  # XPath du champ mot de passe
    password_field.send_keys("BEJAtechno2025/")  # Remplacez par votre mot de passe

    # Cliquer sur le bouton de validation avec XPath
    login_button = driver.find_element(By.XPATH, '//*[@id="valid_login"]')  # XPath du bouton de validation
    login_button.click()

    # Attendre que la page se charge après la connexion
    time.sleep(3)

    # Étape 1 : Cliquer sur un élément dans un menu déroulant
    menu_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="choix"]/li[1]/a'))
    )
    menu_item.click()
    time.sleep(2)

    # Étape 2 : Sélectionner une option dans le menu déroulant
    select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "bt_select_exportbatch"))
    )
    select = Select(select_element)  # Utiliser la classe Select pour interagir avec le menu déroulant

    # Sélectionner l'option "- Tout secteurs - Exporter les rdvs sur journée"
    select.select_by_visible_text("- Tout secteurs - Exporter les rdvs sur journée")
    time.sleep(2)

    # Étape 3 : Sélectionner la date d'aujourd'hui
    date_picker = driver.find_element(By.XPATH, '//*[@id="div_datestart"]/img')  # XPath du sélecteur de date
    date_picker.click()
    time.sleep(2)

    # Sélectionner la date d'aujourd'hui (cela dépend du widget de date utilisé)
    today_date = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]//a[contains(text(), "Aujourd\'hui")]')  # XPath du bouton "Aujourd'hui"
    today_date.click()
    time.sleep(2)

    # Étape 4 : Cliquer sur une case à cocher
    checkbox = driver.find_element(By.XPATH, '//*[@id="jqgh_listeTech_cb"]')  # XPath de la case à cocher
    checkbox.click()
    time.sleep(2)

    # Étape 5 : Cliquer sur le bouton "Visualiser"
    visu_button = driver.find_element(By.XPATH, '//*[@id="bt_visu_in"]')  # XPath du bouton "Visualiser"
    visu_button.click()
    time.sleep(2)

    # Étape 6 : Cliquer sur le bouton "Télécharger CSV"
    download_button = driver.find_element(By.XPATH, '//*[@id="bt_visu_in"]')  # XPath du bouton de téléchargement
    download_button.click()
    time.sleep(5)  # Attendre que le téléchargement se termine

    print(f"Téléchargement du fichier CSV terminé. Le fichier est enregistré dans : {download_dir}")

finally:
    # Fermer le navigateur
    driver.quit()