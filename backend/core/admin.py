from django.contrib import admin
from core.models import Gantt, GanttStatistics  # Utilisez le bon nom de modèle

# Enregistrez les modèles dans l'interface d'administration
admin.site.register(Gantt)
admin.site.register(GanttStatistics)