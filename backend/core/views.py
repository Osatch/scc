from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Gantt
from .serializers import GanttSerializer

@api_view(['GET'])
def gantt_list(request):
    gantt_data = Gantt.objects.all()
    serializer = GanttSerializer(gantt_data, many=True)
    return Response(serializer.data)

