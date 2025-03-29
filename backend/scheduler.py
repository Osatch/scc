# /scc/backend/scheduler.py

import os
import django
import schedule
import time
import threading
from datetime import datetime, time as dt_time
from django.core.management import call_command

# Configuration de Django : utilisez le module settings situé dans config/settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

def run_import_grdv():
    """
    Lance la commande 'import_grdv' (core/management/commands/import_grdv.py).
    """
    call_command('import_grdv')
    print("Commande 'import_grdv' exécutée avec succès.")

def run_import_ard2():
    """
    Lance la commande 'import_ard2' (core/management/commands/import_ard2.py),
    puis planifie l'exécution de 'sync_relancejj' après 1 minute.
    """
    call_command('import_ard2')
    print("Commande 'import_ard2' exécutée avec succès.")
    # Lancer 'sync_relancejj' 1 minute après
    threading.Timer(60, run_sync_relancejj).start()

def run_sync_relancejj():
    """
    Lance la commande 'sync_relancejj' (votre commande de synchronisation des données).
    Puis planifie l'exécution de 'sync_gantt' 30 secondes après.
    """
    call_command('sync_relancejj')
    print("Commande 'sync_relancejj' exécutée avec succès.")
    # Lancer 'sync_gantt' 30 secondes après
    threading.Timer(30, run_sync_gantt).start()

def run_sync_gantt():
    """
    Lance la commande 'import_gantt' (commande qui importe les interventions dans Gantt).
    """
    call_command('import_gantt')
    print("Commande 'import_gantt' exécutée avec succès (30 secondes après sync_relancejj).")

# Attente du démarrage du scheduler à 6h10
print("Attente du démarrage du scheduler jusqu'à 6h10...")
while True:
    now = datetime.now().time()
    if now >= dt_time(6, 10):
        print("6h10 atteint, démarrage du scheduler.")
        break
    time.sleep(30)

# Planification des tâches :
# - 'import_grdv' s'exécute chaque jour à 6h10.
# - 'import_ard2' s'exécute toutes les 30 minutes.
schedule.every().day.at("06:10").do(run_import_grdv)
schedule.every(30).minutes.do(run_import_ard2)

print("Minuterie active :")
print(" - 'import_grdv' à 6h10")
print(" - 'import_ard2' toutes les 30 minutes")
print(" - 'sync_relancejj' 1 minute après chaque import_ard2")
print(" - 'import_gantt' 30 secondes après chaque sync_relancejj")

# Boucle infinie pour exécuter les tâches planifiées
while True:
    schedule.run_pending()
    time.sleep(60)
