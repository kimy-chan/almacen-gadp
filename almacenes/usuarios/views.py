from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.db import IntegrityError
from .forms import Usuario_formulario



from .models import Usuario, Secretaria, Oficinas, Unidad

from django.http import JsonResponse

from persona.forms import Formulario_persona 

from utils.paginador import paginador_general
from persona.models import Persona 

# Create your views here.

def login_sistema(request):
    if(request.method=='POST'):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None and user.es_activo and user.es_habilitado:
                login(request, user)
                return redirect('index')
        else:
            return render(request, '../usuarios/login.html', {'error_message': 'Credenciales inválidas'})
    else:
        return render(request, 'usuarios/login.html')

def actulizar_cuenta_usuario(request, id_usuario, id_persona):
    usuario= get_object_or_404(Usuario, pk=id_usuario)
    persona = get_object_or_404(Persona,pk=id_persona)
    formulario_persona= Formulario_persona(request.POST or None, instance=persona)
    usuario_formulario= Usuario_formulario(request.POST or None, instance=usuario)
    if request.method=='POST':
        if formulario_persona.is_valid() and usuario_formulario.is_valid():
            formulario_persona.save()
            usuario= usuario_formulario.save(commit=False)
            usuario.set_password(usuario_formulario.cleaned_data['password'])
            usuario.persona=persona
            usuario.save()
            return redirect('listando_usuarios')
    context={
        'usuario':usuario,
        'persona':persona,
        'form_persona':formulario_persona,
        'form_usuario':usuario_formulario
    }

    return render(request, 'usuarios/actulizar_cuenta_formulario.html', context)

    

def creando_usuario(request):
    if(request.method=="POST"):
        formulario_u = Usuario_formulario(request.POST)
        formulario_p = Formulario_persona(request.POST)
        if formulario_u.is_valid() and  formulario_p.is_valid():
            persona= formulario_p.save()
            usuario= formulario_u.save(commit=False)
            usuario.set_password(formulario_u.cleaned_data['password'])
            usuario.persona=persona
            usuario.save()
          
        else:
            formulario_u= Usuario_formulario(request.POST)
            formulario_p = Formulario_persona(request.POST)
    else:
        formulario_u= Usuario_formulario()
        formulario_p = Formulario_persona()
    context={'form_usuario':formulario_u,
             'form_persona':formulario_p,
             }
    return render(request, 'usuarios/crear_cuenta_formulario.html', context)


def crear_secretaria_listar(request):
    if(request.method == 'POST'):
        secretaria_post = request.POST.get('secretaria','').strip() 
        if not secretaria_post:
             return JsonResponse({"error":'este campo es obligatorio'})
        try:
            secretaria = Secretaria(secretaria=secretaria_post)
            secretaria.save()
            return JsonResponse({"data": True})
        except IntegrityError:
            return JsonResponse({"error": "El valor  ya existe"})

    else:
        secretatias = list(Secretaria.objects.all().values())   
        return JsonResponse({'data':secretatias}, safe=False)
def Crear_unidad_secretaria(request):
    if request.method== 'POST':
        unidad = request.POST.get('unidad')
        id_secretaria = request.POST.get('secretaria_id')
        if not unidad and id_secretaria:
             return JsonResponse({'error':'campos obligatorios'})
        secretaria=get_object_or_404(Secretaria, pk=id_secretaria)
        try:
            unidad= Unidad.objects.create(nombre=unidad, secretaria=secretaria)
            unidad.save()
            oficina_exists = Oficinas.objects.filter(nombre='Ninguna').exists()
            if not oficina_exists:
                oficina= Oficinas.objects.create(nombre='Ninguna', unidad= unidad)
                oficina.save()
            return JsonResponse({'data':True})
        except IntegrityError:
            return JsonResponse({"error": "El valor  ya existe"})
    
def crear_unidad_listar(request):
    if request.method == 'POST':
        unidad= request.POST['unidad']
        print(unidad)
        if not unidad:
            return JsonResponse({'error':'Este campo es obligatorio'})
        try:   
            unidad= Unidad.objects.create(nombre=unidad)
            unidad.save()
            return JsonResponse({'data':True})
        except IntegrityError:
            return JsonResponse({"error": "El valor  ya existe"})
    else:
        unidad= list(Unidad.objects.all().values())
        return JsonResponse({'data':unidad})
    

def oficinas_listar(request, id_unidad):
    oficinas= list(Oficinas.objects.filter(unidad=id_unidad).values())
    return JsonResponse({'data':oficinas})

def crear_oficinas(request):
    if request.method == 'POST':
        oficinas= request.POST['oficina']
        unidad= request.POST['unidad']
        if not oficinas:
            return JsonResponse({'error':'Este campo es obligatorio'})
        try:   
            unidad = get_object_or_404(Unidad, pk= unidad)
            oficinas= Oficinas.objects.create(nombre=oficinas, unidad=unidad)
            oficinas.save()
            return JsonResponse({'data':True})
        except IntegrityError:
            return JsonResponse({"error": "El valor  ya existe"})






def listando_usuarios(request):
    listado_cuentas_usuarios = Usuario.objects.select_related('persona').filter(es_habilitado=True)
    listado_cuentas_usuarios = paginador_general(request, listado_cuentas_usuarios)
    context={
        'data':listado_cuentas_usuarios,
       
    }
    return render(request, 'usuarios/mostrar_cuentas.html', context)

def soft_delete(request, id):
    usuario= get_object_or_404(Usuario, pk=id)
    usuario.es_habilitado=False
    usuario.save()
    return redirect('listando_usuarios')

def desactivar_cuenta(request, id):
    usuario= get_object_or_404(Usuario, pk=id)
    usuario.es_activo= False
    usuario.save()
    return redirect('listando_usuarios')

def activar_cuenta(request, id):
    usuario= get_object_or_404(Usuario, pk=id)
    usuario.es_activo= True
    usuario.save()
    return redirect('listando_usuarios')

def logout_view(request):
    logout(request)
    return redirect('login')

def crear_ruta_pedido(request):
    return render(request,'usuarios/rutas.pedidos.html')