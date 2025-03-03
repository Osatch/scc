from rest_framework import serializers
from .models import Gantt

class GanttSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gantt
        fields = '__all__'
