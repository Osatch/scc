from rest_framework import serializers
from .models import Gantt
from .models import ARD2

class GanttSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gantt
        fields = '__all__'

class ARD2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ARD2
        fields = '__all__'