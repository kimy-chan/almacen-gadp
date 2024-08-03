from django import forms
from .models import Persona

class Formulario_persona(forms.ModelForm):
    class Meta:
        model = Persona
        fields  ='__all__'
        widgets={
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula_identidad': forms.TextInput(attrs={'class': 'form-control'}),
        }