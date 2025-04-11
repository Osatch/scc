import os
import django
import time
import schedule
import subprocess
from django.core.management import call_command

# Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

def run_all_sync_commands():
    print("\n===== DÉMARRAGE DE LA SYNCHRONISATION =====\n")
    try:
        call_command('import_grdv')
        call_command('import_ard2')
        call_command('sync_relancejj')
        call_command('import_gantt')
        call_command('sync_controlphoto')
        call_command('sync_dr')
        call_command('sync_ds')
    except Exception as e:
        print(f"⚠️ Erreur lors de la synchronisation : {e}")
    print("\n===== SYNCHRONISATION TERMINÉE =====\n")

def run_grdv_bot():
    print("\n🤖 Lancement du bot GRDV (Selenium)...")
    try:
        subprocess.run(["python", "backend/Bot/grdv.py"], check=True)
        print("✅ Bot GRDV exécuté avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur GRDV bot : {e}")

# Planification du bot GRDV à 06:00 chaque jour
schedule.every().day.at("06:00").do(run_grdv_bot)

print("🕒 Scheduler initialisé.")
print(" - 📅 Bot GRDV programmé tous les jours à 06:00.")
print(" - 🔁 Synchronisation complète toutes les 1 minutes.")

# Boucle principale : exécute run_all_sync_commands toutes les 10 minutes, + scheduler
if __name__ == "__main__":
    while True:
        run_all_sync_commands()        # Lancement immédiat des commandes Django
        for _ in range(1):            # Attente de 1 minutes, vérifie toutes les minutes le planificateur
            schedule.run_pending()     # Lance le bot GRDV si l’heure correspond
            time.sleep(60)
