from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Gantt, GanttStatistics, ARD2, Parametres, RelanceJJ, NOK
from .serializers import GanttSerializer, GanttStatisticsSerializer, ARD2Serializer, ParametresSerializer, RelanceJJSerializer, NOKSerializer

# Vue pour la liste des interventions Gantt
@api_view(['GET'])
def gantt_list(request):
    gantt_data = Gantt.objects.all()
    serializer = GanttSerializer(gantt_data, many=True)
    return Response(serializer.data)

# Vue pour les détails d'une intervention Gantt
@api_view(['GET'])
def gantt_detail(request, pk):
    gantt_entry = get_object_or_404(Gantt, pk=pk)
    serializer = GanttSerializer(gantt_entry)
    return Response(serializer.data)

# Vue pour la liste des statistiques Gantt
@api_view(['GET'])
def gantt_statistics_list(request):
    statistics_data = GanttStatistics.objects.all()
    serializer = GanttStatisticsSerializer(statistics_data, many=True)
    return Response(serializer.data)

# Vue pour les détails des statistiques Gantt
@api_view(['GET'])
def gantt_statistics_detail(request, pk):
    statistics_entry = get_object_or_404(GanttStatistics, pk=pk)
    serializer = GanttStatisticsSerializer(statistics_entry)
    return Response(serializer.data)

# Vue pour la connexion
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

# Vue pour la déconnexion
@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

# Vue pour la liste des interventions ARD2
@api_view(['GET'])
def ard2_list(request):
    """Retourne la liste des interventions ARD2 avec date d'importation"""
    ard2_data = ARD2.objects.all().order_by('-date_importation')
    serializer = ARD2Serializer(ard2_data, many=True)
    return Response(serializer.data)

# Vue pour la liste des paramètres
@api_view(['GET'])
def parametres_list(request):
    """Retourne la liste des paramètres"""
    parametres = Parametres.objects.all().order_by('id_tech')
    serializer = ParametresSerializer(parametres, many=True)
    return Response(serializer.data)

# Vue pour la liste des relances JJ
@api_view(['GET'])
def relancejj_list(request):
    """Retourne la liste des relances"""
    relances = RelanceJJ.objects.all().order_by('-date_intervention')
    serializer = RelanceJJSerializer(relances, many=True)
    return Response(serializer.data)

# ======================= VUES POUR NOK =======================

# Vue pour récupérer la liste des enregistrements NOK
@api_view(['GET', 'POST'])
def nok_list(request):
    if request.method == 'GET':
        noks = NOK.objects.all().order_by('-date_rdv')  # Trier par date de RDV descendante
        serializer = NOKSerializer(noks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NOKSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Vue pour récupérer, mettre à jour ou supprimer un enregistrement NOK
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
