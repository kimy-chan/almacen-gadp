from django import forms
from .models import Categoria, Materiales

class Formulario_materiales(forms.ModelForm):
    class Meta:
        model=Materiales
        fields = ['nombre', 'codigo','codigo_paquete' , 'marca', 'cantidad_paquete', 'cantidad_paquete_unidad', 'precio_paquete','precio_unidad',  'tamaño', 'color', 'unidad_medida', 'material', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_paquete': forms.TextInput(attrs={'class': 'form-control'}),
            'tamaño': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_paquete': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_paquete_unidad': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_paquete': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_unidad': forms.TextInput(attrs={'class': 'form-control'})
        }
     
    def __init__(self, *args, **kwargs):#mostrando en un select todas las categorias disponibles
        super(Formulario_materiales,self).__init__(*args, **kwargs)
        categorias_disponibles = [(categoria.id, categoria.nombre) for categoria in Categoria.objects.all()]#consultado a la base de datos     
        self.fields['categoria'].widget = forms.Select(choices=categorias_disponibles, attrs={'class': 'form-select'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-select'})

        instance = kwargs.get('instance')
        if instance:
            # Establecer campos de solo lectura
            self.fields['codigo'].widget.attrs['readonly'] = True
            self.fields['codigo_paquete'].widget.attrs['readonly'] = True
class Formulario_categoria(forms.ModelForm):
    class Meta:
        model=Categoria
        fields =['nombre','codigo_clasificacion']
        widgets = {
            'codigo_clasificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

        
