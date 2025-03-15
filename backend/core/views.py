from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.management import call_command
from django.contrib.auth import authenticate
import io

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Gantt, GanttStatistics, ARD2, Parametres, RelanceJJ, NOK,
    ControlPhoto, Controlafroid, DebriefRACC, DebriefSAV,
    InterventionsSAV, InterventionsRACC
)
from .serializers import (
    GanttSerializer, GanttStatisticsSerializer, ARD2Serializer, ParametresSerializer,
    RelanceJJSerializer, NOKSerializer, ControlPhotoSerializer, ControlafroidSerializer,
    DebriefRACCSerializer, DebriefSAVSerializer, InterventionsSAVSerializer, InterventionsRACCSerializer
)
from .forms import ParametresForm

# ======================= VUES POUR INTERVENTIONS RACC =======================

@api_view(['GET', 'POST'])
def interventionsracc_list(request):
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
    gantt_data = Gantt.objects.all()
    serializer = GanttSerializer(gantt_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def gantt_detail(request, pk):
    gantt_entry = get_object_or_404(Gantt, pk=pk)
    serializer = GanttSerializer(gantt_entry)
    return Response(serializer.data)

@api_view(['GET'])
def gantt_statistics_list(request):
    statistics_data = GanttStatistics.objects.all()
    serializer = GanttStatisticsSerializer(statistics_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def gantt_statistics_detail(request, pk):
    statistics_entry = get_object_or_404(GanttStatistics, pk=pk)
    serializer = GanttStatisticsSerializer(statistics_entry)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

# Nouvelle vue pour retourner le profil de l'utilisateur
@api_view(['GET'])
def user_profile(request):
    if request.user.is_authenticated:
        return Response({'name': request.user.username})
    else:
        return Response({'name': 'Utilisateur non connecté'}, status=401)

@api_view(['GET'])
def ard2_list(request):
    ard2_data = ARD2.objects.all().order_by('-date_importation')
    serializer = ARD2Serializer(ard2_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def parametres_list(request):
    parametres = Parametres.objects.all().order_by('id_tech')
    serializer = ParametresSerializer(parametres, many=True)
    return Response(serializer.data)

def ajouter_parametre(request):
    if request.method == 'POST':
        form = ParametresForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_parametres')
    else:
        form = ParametresForm()
    return render(request, 'ajouter_parametre.html', {'form': form})

@api_view(['GET'])
def relancejj_list(request):
    relances = RelanceJJ.objects.all().order_by('-date_intervention')
    serializer = RelanceJJSerializer(relances, many=True)
    return Response(serializer.data)

# ======================= VUES POUR NOK =======================

@api_view(['GET', 'POST'])
def nok_list(request):
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

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def import_ard2(request):
    try:
        output = io.StringIO()
        call_command('import_ard2', stdout=output)
        return JsonResponse({'status': 'success', 'message': output.getvalue()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_POST
def import_grdv(request):
    try:
        output = io.StringIO()
        call_command('import_grdv', stdout=output)
        return JsonResponse({'status': 'success', 'message': output.getvalue()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
