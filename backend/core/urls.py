from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    gantt_list,            # Vue pour la liste des interventions Gantt
    login_view, logout_view,  # Vues pour la gestion de l'authentification
    ard2_list,             # Vue pour la liste des ARD2
    user_profile,
    parametres_list,       # Vue pour la liste des paramètres
    parametre_detail,      # Vue pour le détail d'un paramètre
    relancejj_list,        # Vue pour la liste des relances JJ
    gantt_statistics_list, # Vue pour la liste des statistiques Gantt
    gantt_detail,          # Vue pour les détails d'une intervention Gantt
    gantt_statistics_detail,  # Vue pour les détails des statistiques Gantt
    nok_list, nok_detail,  # Vues pour la gestion des NOK
    controlphoto_list, controlphoto_detail,  # Vues pour la gestion des ControlPhoto
    controlafroid_list, controlafroid_detail,  # Vues pour la gestion des Controlafroid
    debriefracc_list, debriefracc_detail,  # Vues pour la gestion des DebriefRACC
    debriefsav_list, debriefsav_detail,  # Vues pour la gestion des DebriefSAV
    interventionssav_list, interventionssav_detail,  # Vues pour la gestion des InterventionsSAV
    import_ard2, import_grdv, sync_relancejj, import_parametres, import_gantt, protected_view,  # Vues pour lancer les imports et la protection
    commentaire_list,
    commentaire_detail,  # Vues de commentaire 
    upload_ard_file,
    upload_and_process_ard,# historique ard2 
)

urlpatterns = [
    # Endpoints pour JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Endpoint protégé
    path("protected-endpoint/", protected_view, name="protected-endpoint"),
    
    # Authentification
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # ARD2
    path('ard2/', ard2_list, name='ard2-list'),
    
    # Paramètres
    path('parametres/', parametres_list, name='parametres-list'),
    path('parametres/<int:pk>/', parametre_detail, name='parametre-detail'),
    
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
    
    # User profile
    path('user/profile/', user_profile, name='user_profile'),
    
    # Endpoints d'import
    path('import_ard2/', import_ard2, name='import_ard2'),
    path('import_grdv/', import_grdv, name='import_grdv'),
    path('sync_relancejj/', sync_relancejj, name='sync_relancejj'),
    path('import_parametres/', import_parametres, name='import_parametres'),
    path('import_gantt/', import_gantt, name='import_gantt'),
    
    # Commentaire
    path('commentaires/', commentaire_list, name='commentaire_list'),
    path('commentaires/<int:pk>/', commentaire_detail, name='commentaire_detail'),

    #import ard2 file le csv
    path('upload_ard_file/', upload_ard_file),
    #l'import 
    path('upload_and_process_ard/', upload_and_process_ard, name='upload_and_process_ard'),
]
