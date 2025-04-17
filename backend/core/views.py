from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.core.management import call_command
from django.contrib.auth import authenticate
import io
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Gantt, GanttStatistics, ARD2, Parametres, RelanceJJ, NOK,
    ControlPhoto, Controlafroid, DebriefRACC, DebriefSAV,
    InterventionsSAV, InterventionsRACC, Commentaire, Parametres
)
from .serializers import (
    GanttSerializer, GanttStatisticsSerializer, ARD2Serializer, ParametresSerializer,
    RelanceJJSerializer, NOKSerializer, ControlPhotoSerializer, ControlafroidSerializer,
    DebriefRACCSerializer, DebriefSAVSerializer, InterventionsSAVSerializer, InterventionsRACCSerializer,
    CommentaireSerializer, ParametresSerializer
)
from .forms import ParametresForm
from django.conf import settings
import os

# ======================= VUES POUR INTERVENTIONS RACC =======================
@api_view(['GET', 'POST'])
def interventionsracc_list(request):
    """
    Liste et création des interventions RACC.
    """
    if request.method == 'GET':
        interventions = InterventionsRACC.objects.all().order_by('-date_intervention')
        serializer = InterventionsRACCSerializer(interventions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = InterventionsRACCSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def interventionsracc_detail(request, pk):
    """
    Détail, mise à jour et suppression d'une intervention RACC.
    """
    intervention = get_object_or_404(InterventionsRACC, pk=pk)
    if request.method == 'GET':
        serializer = InterventionsRACCSerializer(intervention)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = InterventionsRACCSerializer(intervention, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        intervention.delete()
        return Response({"message": "Intervention RACC supprimée avec succès"}, status=204)

# ======================= AUTRES VUES EXISTANTES =======================
@api_view(['GET'])
def gantt_list(request):
    """
    Liste des entrées Gantt.
    """
    gantt_data = Gantt.objects.all()
    serializer = GanttSerializer(gantt_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def gantt_detail(request, pk):
    """
    Détail d'une entrée Gantt.
    """
    gantt_entry = get_object_or_404(Gantt, pk=pk)
    serializer = GanttSerializer(gantt_entry)
    return Response(serializer.data)

#ici le form de gantt 
@api_view(['PATCH'])
def gantt_partial_update(request, pk):
    """
    Mise à jour partielle d'un objet Gantt (pour motif/commentaire/validation).
    """
    gantt = get_object_or_404(Gantt, pk=pk)
    serializer = GanttSerializer(gantt, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def gantt_statistics_list(request):
    """
    Liste des statistiques Gantt.
    """
    statistics_data = GanttStatistics.objects.all()
    serializer = GanttStatisticsSerializer(statistics_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def gantt_statistics_detail(request, pk):
    """
    Détail d'une statistique Gantt.
    """
    statistics_entry = get_object_or_404(GanttStatistics, pk=pk)
    serializer = GanttStatisticsSerializer(statistics_entry)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint pour l'authentification. Retourne un token JWT et le rôle de l'utilisateur
    si les identifiants sont corrects. Utilise l'email comme identifiant.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    # ⚠️ Correction ici : on passe email=email (et non username=email)
    user = authenticate(request, email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role,
            'email': user.email
        })
    else:
        return Response({'error': "Identifiants invalides"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def logout_view(request):
    """
    Déconnexion de l'utilisateur en blacklistant le refresh token.
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Retourne le profil de l'utilisateur connecté.
    """
    return Response({'name': request.user.email})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    Vue protégée qui affiche les headers reçus et le nom de l'utilisateur connecté.
    """
    print(request.headers)
    return Response({'message': 'Bienvenue dans la vue protégée !', 'user': request.user.username})

@api_view(['GET'])
def ard2_list(request):
    """
    Liste des enregistrements ARD2.
    """
    ard2_data = ARD2.objects.all().order_by('-date_importation')
    serializer = ARD2Serializer(ard2_data, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def parametres_list(request):
    """
    Endpoint pour récupérer la liste des paramètres et en créer un nouveau.
    """
    if request.method == 'GET':
        parametres = Parametres.objects.all().order_by('id_tech')
        serializer = ParametresSerializer(parametres, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ParametresSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def parametre_detail(request, pk):
    """
    Endpoint pour récupérer, mettre à jour ou supprimer un paramètre spécifique via son identifiant.
    """
    parametre = get_object_or_404(Parametres, pk=pk)
    if request.method == 'GET':
        serializer = ParametresSerializer(parametre)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ParametresSerializer(parametre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        parametre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def relancejj_list(request):
    """
    Liste des relances JJ.
    """
    relances = RelanceJJ.objects.all().order_by('-date_rdv')
    serializer = RelanceJJSerializer(relances, many=True)
    return Response(serializer.data)

# ======================= ENDPOINTS POUR COMMENTAIRES =======================
@api_view(['GET', 'POST'])
def commentaire_list(request):
    """
    Liste et création de commentaires.
    Les commentaires sont triés par date et heure de création de manière décroissante.
    """
    if request.method == 'GET':
        commentaires = Commentaire.objects.all().order_by('-created_date', '-created_time')
        serializer = CommentaireSerializer(commentaires, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def commentaire_detail(request, pk):
    """
    Détail, mise à jour et suppression d'un commentaire.
    """
    commentaire = get_object_or_404(Commentaire, pk=pk)
    if request.method == 'GET':
        serializer = CommentaireSerializer(commentaire)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentaireSerializer(commentaire, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        commentaire.delete()
        return Response({"message": "Commentaire supprimé avec succès"}, status=204)

# ======================= VUES POUR NOK =======================
@api_view(['GET', 'POST'])
def nok_list(request):
    """
    Liste et création des enregistrements NOK.
    """
    if request.method == 'GET':
        noks = NOK.objects.all().order_by('-date_rdv')
        serializer = NOKSerializer(noks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = NOKSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def nok_detail(request, pk):
    """
    Détail, mise à jour et suppression d'un enregistrement NOK.
    """
    nok = get_object_or_404(NOK, pk=pk)
    if request.method == 'GET':
        serializer = NOKSerializer(nok)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = NOKSerializer(nok, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        nok.delete()
        return Response({"message": "NOK supprimé avec succès"}, status=204)

# ======================= VUES POUR CONTROLPHOTO =======================
@api_view(['GET', 'POST'])
def controlphoto_list(request):
    """
    Liste et création des enregistrements ControlPhoto.
    """
    if request.method == 'GET':
        controlphotos = ControlPhoto.objects.all().order_by('-date')
        serializer = ControlPhotoSerializer(controlphotos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ControlPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def controlphoto_detail(request, pk):
    """
    Détail, mise à jour et suppression d'un enregistrement ControlPhoto.
    """
    controlphoto = get_object_or_404(ControlPhoto, pk=pk)
    
    if request.method == 'GET':
        serializer = ControlPhotoSerializer(controlphoto)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ControlPhotoSerializer(controlphoto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        controlphoto.delete()
        return Response({"message": "ControlPhoto supprimé avec succès"}, status=204)

# ======================= VUES POUR CONTROLAFROID =======================
@api_view(['GET', 'POST'])
def controlafroid_list(request):
    """
    Liste et création des enregistrements Controlafroid.
    """
    if request.method == 'GET':
        controlafroids = Controlafroid.objects.all().order_by('-control_photo__date')
        serializer = ControlafroidSerializer(controlafroids, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ControlafroidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def controlafroid_detail(request, pk):
    """
    Détail, mise à jour et suppression d'un enregistrement Controlafroid.
    """
    controlafroid = get_object_or_404(Controlafroid, pk=pk)
    if request.method == 'GET':
        serializer = ControlafroidSerializer(controlafroid)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ControlafroidSerializer(controlafroid, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        controlafroid.delete()
        return Response({"message": "Controlafroid supprimé avec succès"}, status=204)

# ======================= VUES POUR DEBRIEFRACC =======================
@api_view(['GET', 'POST'])
def debriefracc_list(request):
    """
    Liste et création des enregistrements Debrief RACC.
    """
    if request.method == 'GET':
        debriefraccs = DebriefRACC.objects.all().order_by('-date')
        serializer = DebriefRACCSerializer(debriefraccs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DebriefRACCSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def debriefracc_detail(request, pk):
    """
    Détail, mise à jour et suppression d'un enregistrement Debrief RACC.
    """
    debriefracc = get_object_or_404(DebriefRACC, pk=pk)
    if request.method == 'GET':
        serializer = DebriefRACCSerializer(debriefracc)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DebriefRACCSerializer(debriefracc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        debriefracc.delete()
        return Response({"message": "DebriefRACC supprimé avec succès"}, status=204)

# ======================= VUES POUR DEBRIEFSAV =======================
@api_view(['GET', 'POST'])
def debriefsav_list(request):
    """
    Liste et création des enregistrements Debrief SAV.
    """
    if request.method == 'GET':
        debriefsavs = DebriefSAV.objects.all().order_by('-date')
        serializer = DebriefSAVSerializer(debriefsavs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DebriefSAVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def debriefsav_detail(request, pk):
    """
    Détail, mise à jour et suppression d'un enregistrement Debrief SAV.
    """
    debriefsav = get_object_or_404(DebriefSAV, pk=pk)
    if request.method == 'GET':
        serializer = DebriefSAVSerializer(debriefsav)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DebriefSAVSerializer(debriefsav, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        debriefsav.delete()
        return Response({"message": "DebriefSAV supprimé avec succès"}, status=204)

# ======================= VUES POUR INTERVENTIONSSAV =======================
@api_view(['GET', 'POST'])
def interventionssav_list(request):
    """
    Liste et création des interventions SAV.
    """
    if request.method == 'GET':
        interventions = InterventionsSAV.objects.all().order_by('-date_intervention')
        serializer = InterventionsSAVSerializer(interventions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = InterventionsSAVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def interventionssav_detail(request, pk):
    """
    Détail, mise à jour et suppression d'une intervention SAV.
    """
    intervention = get_object_or_404(InterventionsSAV, pk=pk)
    if request.method == 'GET':
        serializer = InterventionsSAVSerializer(intervention)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = InterventionsSAVSerializer(intervention, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        intervention.delete()
        return Response({"message": "Intervention SAV supprimée avec succès"}, status=204)

# ======================= ENDPOINTS D'IMPORT =======================
@csrf_exempt
@require_POST
def import_ard2(request):
    """
    Exécute la commande d'importation ARD2 et retourne le résultat.
    """
    try:
        output = io.StringIO()
        call_command('import_ard2', stdout=output)
        return JsonResponse({'status': 'success', 'message': output.getvalue()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_POST
def import_grdv(request):
    """
    Exécute la commande d'importation GRDV et retourne le résultat.
    """
    try:
        output = io.StringIO()
        call_command('import_grdv', stdout=output)
        return JsonResponse({'status': 'success', 'message': output.getvalue()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_POST
def sync_relancejj(request):
    """
    Exécute la commande de synchronisation des relances JJ et retourne le résultat.
    """
    try:
        output = io.StringIO()
        call_command('sync_relancejj', stdout=output)
        return JsonResponse({'status': 'success', 'message': output.getvalue()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_POST
def import_parametres(request):
    """
    Exécute la commande d'importation des paramètres et retourne le résultat.
    """
    try:
        output = io.StringIO()
        call_command('import_parametres', stdout=output)
        return JsonResponse({'status': 'success', 'message': output.getvalue()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_POST
def import_gantt(request):
    """
    Exécute la commande d'importation Gantt avec une date et retourne le résultat.
    La date doit être transmise en paramètre GET, par exemple ?date=2025-03-22.
    """
    date = request.GET.get('date')
    if not date:
        return JsonResponse({'status': 'error', 'message': 'Paramètre "date" requis.'}, status=400)
    try:
        output = io.StringIO()
        call_command('import_gantt', date=date, stdout=output)
        return JsonResponse({'status': 'success', 'message': output.getvalue()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
@csrf_exempt
@require_POST
def upload_ard_file(request):
    """
    Reçoit un fichier CSV depuis le frontend et le sauvegarde dans backend/Bot/ard2/
    """
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return JsonResponse({'status': 'error', 'message': 'Aucun fichier fourni.'}, status=400)

    try:
        save_dir = os.path.join(settings.BASE_DIR, 'Bot', 'ard2')
        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(save_dir, uploaded_file.name)

        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return JsonResponse({'status': 'success', 'message': f'Fichier sauvegardé dans {save_path}'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


#--------------------------------------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_and_process_ard(request):
    from datetime import date
    import time, io, os
    from django.conf import settings
    from .models import ImportARDLog
    from .serializers import ImportARDLogSerializer
    from django.core.management import call_command

    try:
        # 📁 Trouver le dernier fichier CSV dans Bot/ard2
        save_dir = os.path.join(settings.BASE_DIR, 'Bot', 'ard2')
        os.makedirs(save_dir, exist_ok=True)

        csv_files = [f for f in os.listdir(save_dir) if f.endswith('.csv')]
        if not csv_files:
            return Response({'status': 'error', 'message': 'Aucun fichier CSV trouvé.'}, status=404)

        latest_file = sorted(csv_files, key=lambda x: os.path.getmtime(os.path.join(save_dir, x)), reverse=True)[0]
        latest_path = os.path.join(save_dir, latest_file)

        start_time = time.time()

        # 🛠 Exécution des scripts Django
        output = io.StringIO()
        call_command('import_ard2', stdout=output)
        call_command('sync_relancejj', stdout=output)
        call_command('import_gantt', date=str(date.today()), stdout=output)
        call_command('sync_controlphoto', stdout=output)
        call_command('sync_dr', stdout=output)
        call_command('sync_ds', stdout=output)

        duration = round(time.time() - start_time, 2)

        # 📝 Log en base
        log = ImportARDLog.objects.create(
            fichier_nom=latest_file,
            duree=duration,
            resultat=output.getvalue(),
            utilisateur=request.user
        )

        return Response({
            'status': 'success',
            'message': '✅ Mise à jour effectuée avec succès.',
            'duration': duration,
            'log': ImportARDLogSerializer(log).data
        })

    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)
