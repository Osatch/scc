import os
import django
import schedule
import time
import subprocess
from django.core.management import call_command

# Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

def run_sync_global():
    """Exécute la commande globale de synchronisation."""
    print("Lancement de la commande 'sync_global'...")
    call_command('sync_global')
    print("Commande 'sync_global' exécutée avec succès.")

def run_grdv_bot():
    """Lance le script grdv.py avec Python."""
    print("Lancement du bot GRDV (Selenium)...")
    try:
        subprocess.run(
            ["python", "backend/Bot/grdv.py"],
            check=True
        )
        print("Bot GRDV exécuté avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de grdv.py : {e}")

# Planifications
schedule.every(5).minutes.do(run_sync_global)            # Toutes les 5 minutes
schedule.every().day.at("06:00").do(run_grdv_bot)        # Tous les jours à 06h00

print("Scheduler démarré :")
print(" - 'sync_global' toutes les 5 minutes")
print(" - 'grdv.py' tous les jours à 06h00")

# Boucle principale
while True:
    schedule.run_pending()
    time.sleep(60)
