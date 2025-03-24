# core/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    gantt_list,            # Vue pour la liste des interventions Gantt
    login_view, logout_view,  # Vues pour la gestion de l'authentification
    ard2_list,             # Vue pour la liste des ARD2
     user_profile,
    parametres_list,       # Vue pour la liste des paramètres
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
    import_ard2, import_grdv, protected_view # Vues pour lancer les imports

)

urlpatterns = [

   # Endpoint pour obtenir un token (obtain pair : access et refresh)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint pour rafraîchir le token d'accès
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Endpoint protégé, accessible uniquement si le token est fourni
    path("protected-endpoint/", protected_view, name="protected-endpoint"),


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

    # Endpoints d'import
    path('user/profile/', user_profile, name='user_profile'),
    path('api/protected/', protected_view, name='protected-endpoint'),
    path('import_ard2/', import_ard2, name='import_ard2'),
    path('import_grdv/', import_grdv, name='import_grdv'),
    path('sync_relancejj/', import_grdv, name='sync_relancejj'),

]