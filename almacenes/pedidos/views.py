from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import   login_required
import random
from materiales.models import Materiales
from django.db.models import Q
from utils.paginador import paginador_general
from usuarios.models import Usuario
from  utils.paginador import paginador_general
from django.urls import reverse
from datetime import datetime
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from datetime import datetime


from .models import Pedido, Autorizacion_pedido

def index(request):
   

    pedido_pendiente= lista_pedidos_por_estado(request,'pendiente')
    nombre_categoria='materiales'
    if (request.method == 'POST'):
        id_categoria = request.POST.get('categoria_id')
        if not id_categoria:
            return redirect('index')
        productos_categoria= Materiales.objects.select_related('categoria').filter(categoria_id=id_categoria, es_habilitado=True)
        productos_categoria= paginador_general(request,productos_categoria)
        if productos_categoria and productos_categoria[0].categoria.nombre:
            nombre_categoria = productos_categoria[0].categoria.nombre
        else:
            nombre_categoria = 'materiales'


    else:
        productos_categoria= Materiales.objects.select_related('categoria').filter(es_habilitado=True)
        productos_categoria= paginador_general(request, productos_categoria)
       

    context ={
            'data1':pedido_pendiente,
            'data':productos_categoria,
            'categoria':nombre_categoria
         
                }
    return render(request, 'pedidos/index.html', context)
   



def buscador(request):
    nombre_categoria = 'materiales'
    data_buscador = request.GET.get('buscador','')
    producto  = Materiales.objects.select_related('categoria').filter(Q(nombre__icontains=data_buscador) | Q(codigo__icontains=data_buscador) |  Q(marca__icontains=data_buscador), es_habilitado= True)
    producto = paginador_general(request, producto)
    context={
        'data':producto,
        'categoria':nombre_categoria
    }
    return  render(request, 'pedidos/index.html', context)

def listar_info_material(request,id_material):
  
    material =  get_object_or_404(Materiales, pk=id_material)
    data={
        'id':material.id,
        'codigo':material.codigo,
        'nombre':material.nombre
    }   
    return JsonResponse({"data":data})
#------------------------------

def realizar_pedido(request):
    id_usuario= request.user.id
    if request.method =='POST':
       try:
            id_material=request.POST["id_material"]
            cantidad_pedido =request.POST["cantidad_pedido"]
            if not id_material or not cantidad_pedido:
                 return JsonResponse({"error":"Los campos son obligatorios"})
            usuario = get_object_or_404(Usuario, id=id_usuario)
            material = get_object_or_404(Materiales, id=id_material)
            if int(cantidad_pedido) <=  0:
                return JsonResponse({"error":"Ingrese un numero mayor a 0", })
            if int(cantidad_pedido) > material.stock:
                return JsonResponse({"error":f"Solo queda: {material.stock} en el material: {material.nombre}",})
            total =  material.stock- int(cantidad_pedido)
            pedido= Pedido.objects.create(
                                          cantidad_pedida=int(cantidad_pedido),
                                          usuario=usuario,
                                          material=material)
      
            material.stock= total
            pedido.save()
            material.save()
            return JsonResponse({"data":"Pedido Realizado"})
       except Exception as e:
           print("ERROR", e)
           return JsonResponse({"error":"Ocurrio un error al realiza el pedido"})
           
def generar_numero_unico():
    return random.randint(1000, 9999)

def cambiar_estado_pedido(request):
    if request.method == 'GET':
        ids = request.GET.getlist('id')
        numero = generar_numero_unico()
        for id in ids:
            pedido= get_object_or_404(Pedido, pk=id)
            pedido.estado_de_pedido='realizado'
            pedido.numero_pedido=numero
            pedido.save()    
        return JsonResponse({'status': 'success', 'ids': ids})
    
    # Si la solicitud no es GET, retorna un error
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

#------------------------------
def listar_pedidos(request):
    listando_pedidos = Pedido.objects.filter(aprobado_unidad=True).distinct('usuario')
    context={
       'data':listando_pedidos
    }
    return render(request, 'pedidos/listar_pedido.html', context)

def listando_pedido_almacen(request, id_usuario):
    pedido = Pedido.objects.filter(aprobado_unidad=True, usuario=id_usuario) 
    pedido = paginador_general(request, pedido)      
    context = {
        'data': pedido
        }
    return render(request, 'pedidos/lintando.pedidos.almacen.html', context)

def lista_pedido_por_id(request, id_pedido):
    pedido=get_object_or_404(Pedido, pk= id_pedido)
    data ={
        'id':pedido.id,
        'codigo':pedido.material.codigo,
        'nombre': pedido.material.nombre,
        'cantidad': pedido.cantidad_pedida
        
    }
    return JsonResponse({'data':data})

def realizar_entrega(request):
    if request.method == 'POST':
        id= request.POST['pedido_id']
        cantidad_entregada = request.POST['cantidad_entregada']
        if not cantidad_entregada:
            return JsonResponse({'error':'Campo obligatorio'})
        pedido = get_object_or_404(Pedido,pk= id)
        if int(cantidad_entregada) < 1:
             return JsonResponse({'data':'Cantidad minima es: 1'})
        elif int(cantidad_entregada) > pedido.cantidad_pedida:
            return JsonResponse({'data':f'Cantidad maxima es:{pedido.cantidad_pedida}'})
        
        cantidad_pedida = pedido.cantidad_pedida - int(cantidad_entregada)
        total_stock = pedido.material.stock
        nuevo_stock = total_stock + cantidad_pedida
        pedido.fecha_entrega_salida = datetime.now()
        pedido.cantidad_entrega = cantidad_entregada
        pedido.estado_pedido_almacen ='Completada'
        pedido.material.stock = nuevo_stock
        pedido.save()
        pedido.material.save()
        return JsonResponse({'data':'Enviado'})


def mis_pedidos(request): #muestra los pedidos de cada unidad o secretaria
    pedidos= lista_pedidos_por_estado(request, 'realizado')
    pedidos= paginador_general(request, pedidos)
    context={
        'data':pedidos,
        'title':'Mis pedidos'   
    }
    return render(request, 'pedidos/mis_pedidos.html', context)

def lista_pedidos_por_estado(request,estado):
    id_usuario= request.user.id
    pedidos= Pedido.objects.select_related('usuario').filter(usuario_id=id_usuario, estado_de_pedido=estado).order_by('-fecha_pedido')
    return pedidos

def mostrar_informacion_pedidio_aprobaciones(request,id_pedido):
    if request.method == 'GET':
        data=[]
        pedido = get_object_or_404(Pedido, pk=id_pedido)
        aprobaciones = Autorizacion_pedido.objects.filter(pedido= pedido.id)
        for aprobacion in aprobaciones:
            informacion ={
            'unidad':aprobacion.usuario.unidad.nombre,
            'aprobacion':aprobacion.estado_autorizacion,
            'nombre':aprobacion.usuario.persona.nombre + " " + aprobacion.usuario.persona.apellidos ,
            'oficina':aprobacion.usuario.oficina.nombre,
            'fecha': aprobacion.fecha_de_autorizacion.strftime('%Y-%m-%d') if aprobacion.fecha_de_autorizacion else None
            }
            data.append(informacion)
        print(data)
        return JsonResponse({'data':data})

def eliminar_mi_pedido(request, id_pedido):
    pedido= get_object_or_404(Pedido, pk=id_pedido)
    pedido_autorizado = Autorizacion_pedido.objects.filter(pedido=pedido)
    for p in pedido_autorizado:
        if p.estado_autorizacion == True:
            return redirect(f"{reverse('mis_pedidos')}?error=Este pedido ha sido aprobado y no se puede cancelar")
        continue
    pedido.delete()
    return redirect(f"{reverse('mis_pedidos')}?success=Pedido cancelado correctamente")

def todos_mis_pedidos(request):
    id_usuario= request.user.id
    print(id_usuario)
    pedidos= Pedido.objects.select_related('usuario', 'material').filter(usuario_id=id_usuario).order_by('-fecha_pedido')
    context={
        'data':pedidos,
        'title':'Historial de pedidos'
    }
    return render(request, 'pedidos/mis_pedidos.html', context)

def listar_pedidos_unidad(request, id_usuario):

    usuario = get_object_or_404(Usuario, pk=id_usuario)

    # Verifica si el usuario tiene permiso
    if not usuario.encargado:
        return JsonResponse({"mensaje": "No tienes permiso"}, status=403)

    # Filtra los pedidos por la unidad del usuario
    pedidos_unidad = Pedido.objects.filter(
        usuario__unidad=usuario.unidad
    ).order_by('numero_pedido')


    pedidos_unicos = {}
    for pedido in pedidos_unidad:
        if pedido.numero_pedido not in pedidos_unicos:
            pedidos_unicos[pedido.numero_pedido] = pedido

    pedidos_unicos_list = list(pedidos_unicos.values())


    context = {
        'data': pedidos_unicos_list
    }

    return render(request, 'pedidos/usuarios.pedidos.html', context)

def listar_pedidos_por_codigo(request, numero):
    pedido= Pedido.objects.filter(numero_pedido=numero)
    context = {
        'data': pedido
    }
    return render(request, 'pedidos/listar_pedidos_unidad.html', context)
    
def autorizar_pedidos(request, id_pedido):#autoria el pedido de cada unidad
    print('hola')
    id_usuario= request.user.id
    pedido = get_object_or_404(Pedido,pk=id_pedido)
    numero=pedido.numero_pedido
    usuario = get_object_or_404(Usuario, pk= id_usuario)
    autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= True)
    autorizacion_pedido.save()
    pedido.aprobado_unidad= True
    pedido.save()
    url = reverse('pedido_numero', kwargs={'numero': numero})
    return redirect(f"{url}?success=Pedido autorizado correctamente")
def autorizar_pedidos_almacen(request, id_pedido, id_usuario):#autoriza pedidos el lamacen
    pedido = get_object_or_404(Pedido,pk=id_pedido)
    usuario = get_object_or_404(Usuario, pk= id_usuario)
    autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= True)
    autorizacion_pedido.save()
    pedido.aprobado_almacen= True
    pedido.save()
    return redirect(f"{reverse('informacion_pedido', kwargs={'id_usuario': id_usuario})}?success=Pedido autorizado correctamente")




def rechazar_pedido_unidad(request, id_pedido):
    id_usuario= request.user.id
    pedido = get_object_or_404(Pedido,pk=id_pedido)
    pedido.aprobado_unidad= False
    pedido.save()
    usuario = get_object_or_404(Usuario, pk= id_usuario)
    autorizacion_pedido= Autorizacion_pedido.objects.create(pedido=pedido,usuario= usuario, estado_autorizacion= False)
    autorizacion_pedido.save()
    
    return redirect(f"{reverse('listar_pedidos_unidad', kwargs={'id_usuario': id_usuario})}?pedido_rechazado=Pedido rechazado correctamente")
    




def imprecion_solicitud(request,numero):
    pedido= Pedido.objects.filter(numero_pedido=numero)
    user_pedido = f"{pedido[0].usuario.persona.nombre} { pedido[0].usuario.persona.apellidos }" 
    autorizacion= Autorizacion_pedido.objects.filter(pedido=pedido[0].id)

    user_autorizacion = f"{autorizacion[0].usuario.persona.nombre} { autorizacion[0].usuario.persona.apellidos }" 
    context = {
        'data': pedido,
        'usuario_pedido':user_pedido,
       'user_autorizacion':user_autorizacion
    }
    return render(request, "imprimir/solicitud.html", context)





def generate_pdf(request, numero):
    pedido= Pedido.objects.filter(numero_pedido=numero)
    user_pedido = f"{pedido[0].usuario.persona.nombre} { pedido[0].usuario.persona.apellidos }" 

    context = {
        'data': pedido,
        'usuario_pedido':user_pedido
    }
    html_string = render_to_string('imprimir/solicitud.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedido_materiales.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response




def sub_pedido(request):
    print(request.POST)
    pedido= request.POST['pedido']
    sub_pedido= request.POST['sub_pedido']
    material= request.POST['material']
    material_existente= get_object_or_404(Materiales, pk=material)
    if not sub_pedido:
          return JsonResponse({'data':'Ingrese un valor'})

    if int(sub_pedido) <= 0:
        return JsonResponse({'data':'No se puede asignar material menor a 0'})
    if int(sub_pedido) > material_existente.stock:
        return JsonResponse({'data':'No se puede asignar material mayor al stock'})
    pedido = get_object_or_404(Pedido, pk= pedido)
    


    pedido.sub_cantidad_pedida= sub_pedido

    cantidad_p= pedido.cantidad_pedida
    
    material_existente.stock += cantidad_p
    stock= material_existente.stock - int(sub_pedido)
    material_existente.stock=stock
    material_existente.save()
    pedido.save()
    return JsonResponse({'data':'guardado'})