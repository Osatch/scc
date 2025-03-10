from django.urls import path
from .views import (
    gantt_list,  # Assurez-vous que cette vue existe
    login_view, logout_view,
    ard2_list,
    parametres_list,
    relancejj_list,
    gantt_statistics_list,  # Nouvelle vue pour GanttStatistics
    gantt_detail,  # Nouvelle vue pour les détails d'une intervention Gantt
    gantt_statistics_detail,nok_list, nok_detail  # Ajout des vues NOK  # Nouvelle vue pour les détails des statistiques Gantt
)

urlpatterns = [
    # Routes existantes
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('ARD2/', ard2_list, name='ard2-list'),  # Pour ARD2
    path('parametres/', parametres_list, name='parametres_list'),  # Pour les paramètres
    path('relances/', relancejj_list, name='relancejj-list'),  # Pour les relances

    # Nouvelles routes pour Gantt et GanttStatistics
    path('gantt/', gantt_list, name='gantt-list'),  # Liste des interventions Gantt
    path('gantt/<int:pk>/', gantt_detail, name='gantt-detail'),  # Détails d'une intervention Gantt
    path('gantt-statistics/', gantt_statistics_list, name='gantt-statistics-list'),  # Liste des statistiques Gantt
    path('gantt-statistics/<int:pk>/', gantt_statistics_detail, name='gantt-statistics-detail'),
    
      # Détails des statistiques Gantt

    # Nouvelles routes pour NOK
    path('nok/', nok_list, name='nok-list'),  # Liste des enregistrements NOK
    path('nok/<int:pk>/', nok_detail, name='nok-detail'),  # Détails d'un NOK
]