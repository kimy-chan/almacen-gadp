from materiales.models import Categoria
from usuarios.models import Usuario
from django.shortcuts import redirect

def listado_categorias_sidebar(request):
    categoria= Categoria.objects.all()
    return  {'listado_categoria':categoria}

def user_datos(request):
    if request.user.is_authenticated:
        usuario_id = request.user.id 
        try:
            usuario = Usuario.objects.select_related('persona','unidad').get(pk=usuario_id)
            print(usuario.encargado)
            return {'usuario':usuario}
        except Exception as e:
            return {'usuario':None}
    else:
        return {'usuario':None}
    
