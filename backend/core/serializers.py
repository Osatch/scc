from rest_framework import serializers
from .models import ARD2, Parametres, RelanceJJ, Gantt, GanttStatistics, NOK  # Ajout de NOK

# Sérialiseur pour ARD2
class ARD2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ARD2
        fields = '__all__'

# Sérialiseur pour Parametres
class ParametresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametres
        fields = '__all__'  # Sérialiser tous les champs

# Sérialiseur pour RelanceJJ
class RelanceJJSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelanceJJ
        fields = '__all__'  # Pour inclure tous les champs du modèle

# Sérialiseur pour Gantt
class GanttSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gantt
        fields = '__all__'  # Inclut tous les champs du modèle

# Sérialiseur pour GanttStatistics
class GanttStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GanttStatistics
        fields = '__all__'  # Inclut tous les champs du modèle

# Sérialiseur pour NOK
class NOKSerializer(serializers.ModelSerializer):
    class Meta:
        model = NOK
        fields = '__all__'  # Inclut tous les champs du modèle
