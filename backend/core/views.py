from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Gantt
from .serializers import GanttSerializer
from .models import ARD2
from .serializers import ARD2Serializer

@api_view(['GET'])
def gantt_list(request):
    gantt_data = Gantt.objects.all()
    serializer = GanttSerializer(gantt_data, many=True)
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

#api ard2
@api_view(['GET'])
def ard2_list(request):
    """Retourne la liste des interventions ARD2 avec date d'importation"""
    ard2_data = ARD2.objects.all().order_by('-date_importation')  # Trier par la plus récente
    serializer = ARD2Serializer(ard2_data, many=True)
    return Response(serializer.data)