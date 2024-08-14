from django import forms
from .models import Pedido

class Formualrio_pedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cantidad_pedida','unidad_manejo']
        widgets = {
            'unidad_manejo': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'pieza'}),
            'cantidad_pedido': forms.TextInput(attrs={'class': 'form-control'}),
        }

        
