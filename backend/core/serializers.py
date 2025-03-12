from rest_framework import serializers
from django import forms  # Importez le module forms
from .models import (
    Gantt, GanttStatistics, ARD2, Parametres, RelanceJJ, NOK, ControlPhoto, Controlafroid, DebriefRACC, DebriefSAV
)

# Serializers pour les modèles
class GanttSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gantt
        fields = '__all__'

class GanttStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GanttStatistics
        fields = '__all__'

class ARD2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ARD2
        fields = '__all__'

class ParametresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametres
        fields = '__all__'

class RelanceJJSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelanceJJ
        fields = '__all__'

class NOKSerializer(serializers.ModelSerializer):
    class Meta:
        model = NOK
        fields = '__all__'

class ControlPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlPhoto
        fields = '__all__'

class ControlafroidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controlafroid
        fields = '__all__'

class DebriefRACCSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebriefRACC
        fields = '__all__'

class DebriefSAVSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebriefSAV
        fields = '__all__'

# Formulaire pour le modèle Parametres
class ParametresForm(forms.ModelForm):
    class Meta:
        model = Parametres
        fields = '__all__'
        widgets = {
            'actif_depuis': forms.DateInput(attrs={'type': 'date'}),  # Widget pour le champ de date
        }