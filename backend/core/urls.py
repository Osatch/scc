from django.urls import path
from .views import gantt_list
from .views import login_view, logout_view
from .views import ard2_list
from .views import parametres_list
from .views import relancejj_list


urlpatterns = [
    path('gantt/', gantt_list, name='gantt_list'),  # Accès via /api/gantt/
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('ARD2/', ard2_list, name='ard2-list'), #ca c'est pour ard2
    path('parametres/', parametres_list, name='parametres_list'),#paramètres
     path('relances/', relancejj_list, name='relancejj-list'),#relancejj
    

    
]

