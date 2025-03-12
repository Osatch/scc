from django import forms
from .models import Parametres

class ParametresForm(forms.ModelForm):
    class Meta:
        model = Parametres
        fields = '__all__'
        widgets = {
            'actif_depuis': forms.DateInput(attrs={'type': 'date'}),
        }