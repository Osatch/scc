from django.urls import path
from .views import gantt_list


urlpatterns = [
    path('gantt/', gantt_list, name='gantt_list'),  # Accès via /api/gantt/

    
]
