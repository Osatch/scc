from rest_framework import serializers
from django import forms
from .models import (
    Gantt, GRDV, GanttStatistics, ARD2, Parametres, RelanceJJ, NOK,
    ControlPhoto, Controlafroid, DebriefRACC, DebriefSAV, InterventionsSAV, InterventionsRACC, Commentaire,ImportARDLog,CustomUser
)
# serializers.py admin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'role']

# Serializer pour le modèle Gantt
class GanttSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gantt
        fields = '__all__'

# Serializer pour le modèle GanttStatistics
class GanttStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GanttStatistics
        fields = '__all__'

# Serializer pour le modèle ARD2
class ARD2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ARD2
        fields = '__all__'

# Serializer pour le modèle Parametres
class ParametresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametres
        fields = '__all__'

# Serializer pour le modèle RelanceJJ
class RelanceJJSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelanceJJ
        fields = '__all__'

# Serializer pour le modèle NOK
class NOKSerializer(serializers.ModelSerializer):
    class Meta:
        model = NOK
        fields = '__all__'

# Serializer pour le modèle ControlPhoto
class ControlPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlPhoto
        fields = '__all__'

# Serializer pour le modèle Controlafroid
class ControlafroidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controlafroid
        fields = '__all__'

# Serializer pour le modèle DebriefRACC
class DebriefRACCSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebriefRACC
        fields = '__all__'

# Serializer pour le modèle DebriefSAV
class DebriefSAVSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebriefSAV
        fields = '__all__'

# Serializer pour le modèle InterventionsSAV
class InterventionsSAVSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterventionsSAV
        fields = '__all__'

# Serializer pour le modèle InterventionsRACC
class InterventionsRACCSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterventionsRACC
        fields = '__all__'

# Serializer pour le modèle Commentaire
class CommentaireSerializer(serializers.ModelSerializer):
    # Lecture seule pour afficher le username du commentateur et le jeton_commande lié à RelanceJJ
    commentateur_username = serializers.ReadOnlyField(source='commentateur.username')
    jeton_commande = serializers.ReadOnlyField(source='jeton.jeton_commande')

    class Meta:
        model = Commentaire
        fields = [
            'id', 
            'jeton', 
            'jeton_commande', 
            'commentaire', 
            'commentateur', 
            'commentateur_username',
            'created_date',
            'created_time'
        ]

# Formulaire pour le modèle Parametres
class ParametresForm(forms.ModelForm):
    class Meta:
        model = Parametres
        fields = '__all__'
        widgets = {
            'actif_depuis': forms.DateInput(attrs={'type': 'date'}),
        }

# Serializer pour une réponse protégée
class ProtectedSerializer(serializers.Serializer):
    message = serializers.CharField()


# serializers.py

class ImportARDLogSerializer(serializers.ModelSerializer):
    utilisateur_email = serializers.ReadOnlyField(source='utilisateur.email')

    class Meta:
        model = ImportARDLog
        fields = ['id', 'fichier_nom', 'import_date', 'duree', 'resultat', 'utilisateur_email']

class StatutRetardSerializer(serializers.ModelSerializer):
    pec_retard_par = serializers.ReadOnlyField(source='pec_retard_par.username')
    date_statut_retard = serializers.ReadOnlyField()

    class Meta:
        model = RelanceJJ
        fields = [
            'id',
            'jeton_commande',
            'techniciens',
            'type_statut_retard',
            'details_retard',
            'pec_retard_par',
            'date_statut_retard',
        ]
