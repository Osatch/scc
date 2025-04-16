import os
import django
import time
import schedule
import subprocess
from django.core.management import call_command
from datetime import datetime

# Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

def run_grdv_bot_and_import():
    print("\n🌅 6h00 — Démarrage GRDV Bot + Import...\n")

    try:
        # 1. Lancer le bot
        print("🤖 Lancement du bot GRDV...")
        subprocess.run(["python", "bot/grdv.py"], check=True)
        print("✅ Bot GRDV exécuté avec succès.")

        # 2. Exécuter l'import GRDV
        print("📥 Import des données GRDV via Django...")
        call_command('import_grdv')
        print("✅ Données GRDV importées.")
    except Exception as e:
        print(f"❌ Erreur lors du traitement GRDV : {e}")

# Planification : uniquement à 6h00
schedule.every().day.at("06:00").do(run_grdv_bot_and_import)

print("🕒 Scheduler prêt.")
print(" - ✅ Tous les jours à 06:00 → bot + import_grdv")

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
