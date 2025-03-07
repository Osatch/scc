from rest_framework import serializers
from .models import Gantt
from .models import ARD2
from .models import Parametres
from .models import RelanceJJ

class GanttSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gantt
        fields = '__all__'

class ARD2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ARD2
        fields = '__all__'

class ParametresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametres
        fields = '__all__'  # Sérialiser tous les champs

class RelanceJJSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelanceJJ
        fields = '__all__'  # Pour inclure tous les champs du modèle