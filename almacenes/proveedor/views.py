from django.shortcuts import render, redirect, HttpResponse
from django_countries import countries ##sale de aqui todos los paises
from  persona.models import Persona
from .models import Proveedor
from django.db import transaction
from django.contrib.auth.decorators import login_required

def listar_proveedores(request):
    #id_use=request.user.id   //recuepra el id del usuario
    listar_proveedores = Proveedor.objects.select_related('persona').all()
    return render(request, 'proveedor/index.html',{'proveedores':listar_proveedores})


def formulario_proveedor(request):
    if(request.method == 'POST'):
        empresa = request.POST['empresa']
        nit = request.POST['nit']
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        cedula_identidad = request.POST['cedula_identidad']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        pais = request.POST['pais'] 
     
       
        persona= Persona.objects.create(cedula_identidad= cedula_identidad, nombre= nombre, apellidos= apellidos)
        Proveedor.objects.create(empresa=empresa, nit= nit, correo= correo, telefono=telefono,pais=pais ,direccion= direccion, persona=persona)
       
        
        return redirect('listar_proveedor')
    return  render(request, 'proveedor/formulario.html', {'paises':countries})
def actulizar_proveedor(request):
    return  render(request, 'proveedor/actualizar.formulario.html')
