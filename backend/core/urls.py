from django.urls import path
from .views import (
    gantt_list,  # Vue pour la liste des interventions Gantt
    login_view, logout_view,  # Vues pour la gestion de l'authentification
    ard2_list,  # Vue pour la liste des ARD2
    parametres_list,  # Vue pour la liste des paramètres
    relancejj_list,  # Vue pour la liste des relances JJ
    gantt_statistics_list,  # Vue pour la liste des statistiques Gantt
    gantt_detail,  # Vue pour les détails d'une intervention Gantt
    gantt_statistics_detail,  # Vue pour les détails des statistiques Gantt
    nok_list, nok_detail,  # Vues pour la gestion des NOK
    controlphoto_list, controlphoto_detail,  # Vues pour la gestion des ControlPhoto
    controlafroid_list, controlafroid_detail,  # Vues pour la gestion des Controlafroid
    debriefracc_list, debriefracc_detail,  # Vues pour la gestion des DebriefRACC
    debriefsav_list, debriefsav_detail,  # Vues pour la gestion des DebriefSAV
    interventionssav_list, interventionssav_detail,  # Vues pour la gestion des InterventionsSAV
)

urlpatterns = [
    # Authentification
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # ARD2
    path('ard2/', ard2_list, name='ard2-list'),

    # Paramètres
    path('parametres/', parametres_list, name='parametres-list'),

    # Relances JJ
    path('relances/', relancejj_list, name='relancejj-list'),

    # Gantt
    path('gantt/', gantt_list, name='gantt-list'),
    path('gantt/<int:pk>/', gantt_detail, name='gantt-detail'),

    # Statistiques Gantt
    path('gantt-statistics/', gantt_statistics_list, name='gantt-statistics-list'),
    path('gantt-statistics/<int:pk>/', gantt_statistics_detail, name='gantt-statistics-detail'),

    # NOK
    path('nok/', nok_list, name='nok-list'),
    path('nok/<int:pk>/', nok_detail, name='nok-detail'),

    # ControlPhoto
    path('controlphoto/', controlphoto_list, name='controlphoto-list'),
    path('controlphoto/<int:pk>/', controlphoto_detail, name='controlphoto-detail'),

    # Controlafroid
    path('controlafroid/', controlafroid_list, name='controlafroid-list'),
    path('controlafroid/<int:pk>/', controlafroid_detail, name='controlafroid-detail'),

    # DebriefRACC
    path('debriefracc/', debriefracc_list, name='debriefracc-list'),
    path('debriefracc/<int:pk>/', debriefracc_detail, name='debriefracc-detail'),

    # DebriefSAV
    path('debriefsav/', debriefsav_list, name='debriefsav-list'),
    path('debriefsav/<int:pk>/', debriefsav_detail, name='debriefsav-detail'),

    # InterventionsSAV
    path('interventionssav/', interventionssav_list, name='interventionssav-list'),
    path('interventionssav/<int:pk>/', interventionssav_detail, name='interventionssav-detail'),
]