from django.contrib import admin
from core.models import Gantt, GanttStatistics  # Utilisez le bon nom de modèle
from core.models import ARD2

# Enregistrez les modèles dans l'interface d'administration
admin.site.register(Gantt)
admin.site.register(GanttStatistics)

@admin.register(ARD2)
class ARD2Admin(admin.ModelAdmin):
    list_display = ('jeton_commande', 'technicien', 'departement', 'etat_intervention', 'terminee', 'date_importation')
    list_filter = ('etat_intervention', 'terminee', 'departement')
    search_fields = ('jeton_commande', 'technicien')