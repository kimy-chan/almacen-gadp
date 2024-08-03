from django import forms
from .models import Pedido

class Formualrio_pedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['descripcion','cantidad_pedida','unidad_manejo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control','rows':2}),
            'unidad_manejo': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'pieza'}),
            'cantidad_pedido': forms.TextInput(attrs={'class': 'form-control'}),
        }

        
