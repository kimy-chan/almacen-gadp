
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import Formulario_categoria,Formulario_materiales
from django.http import JsonResponse
from django.http import HttpResponse


from django.template.loader import get_template
from .models import Categoria, Materiales

# Create your views here.

def crear_categoria(request):    
    if(request.method == 'POST'):
        formulario= Formulario_categoria(request.POST)
        if formulario.is_valid():
            formulario.save()
            return JsonResponse({'data':True})
        else:
            formulario= Formulario_categoria(request.POST)
            errors=  dict(formulario.errors.items())
            return JsonResponse({'errores':errors})
    else:
        formulario= Formulario_categoria()  
    categorias = Categoria.objects.all().order_by('-fecha_creacion')
    context={
        'form':formulario,
        'categorias':categorias
    }
    return render(request, 'materiales/categoria/formulario.crear.html', context)

def crear_material(request):
    if(request.method=='POST'):
        formulario= Formulario_materiales(request.POST)
        if(formulario.is_valid()):
            codigo= formulario.cleaned_data['codigo']
            codigo_paquete= formulario.cleaned_data['codigo_paquete']
            categoria= formulario.cleaned_data['categoria']
            material= formulario.save()
            material.codigo_paquete= f"{categoria.codigo_clasificacion}-{codigo_paquete }"
            material.codigo=f"{material.codigo_paquete}-{codigo} "
            material.save()
            material.calcular_total_paquetes()
            material.calcular_precio_total()
        else:
            formulario= Formulario_materiales(request.POST)
    else: 
        formulario= Formulario_materiales()
    context={
        'form':formulario
    }
    return render(request, 'materiales/formulario.material.html', context)


def listado_material(request, id_categoria):#lista todos los material por categoria
    listar_productos_categoria= Materiales.objects.select_related('categoria').filter(categoria_id=id_categoria,es_habilitado=True)
    nombre_categoria = Categoria.objects.get(pk=id_categoria)#trae el nombre de la categoria para el sud titulo
    context={
        'data':listar_productos_categoria,
        'nombre_categoria':nombre_categoria
    }
    return render(request, 'materiales/listar_material.html', context)

def informacion_material(request, id_material):
    info_producto= Materiales.objects.get(pk= id_material)
    context={
        'material':info_producto
    }
    return render(request, 'materiales/informacion_material.html', context)

def editar_material(request, id_material):
    material = get_object_or_404(Materiales, pk=id_material)
    formulario_material = Formulario_materiales(request.POST or None, instance= material)
    if request.method == 'POST':
        if formulario_material.is_valid():
            codigo= formulario_material.cleaned_data['codigo']
            codigo_paquete= formulario_material.cleaned_data['codigo_paquete']
            antiguo_codigo_paquete=codigo_paquete.split('-')
            codigo_antiguo=codigo.split('-')
            categoria= formulario_material.cleaned_data['categoria']
            material= formulario_material.save()
            material.codigo_paquete= f"{categoria.codigo_clasificacion}-{antiguo_codigo_paquete[1]}"
            material.codigo=f"{material.codigo_paquete}-{codigo_antiguo[2]} "
            material.save()
            material.calcular_total_paquetes()
            material.calcular_precio_total()
            return HttpResponse('actulizado')
    
    context={
        'form':formulario_material,
        'material': material

    }
    return render(request, 'materiales/formulario.actulizar.material.html', context)

def softDelete(request, id_material, id_categoria): #elimina el material
    material = get_object_or_404(Materiales, pk= id_material)
    categoria = get_object_or_404(Categoria, pk= id_categoria)
    material.es_habilitado= False
    material.save()
    return  redirect("categorias_por_id", id_categoria=categoria.id)



def inprimir(request, id):
    ruta_tamplate ='materiales/informacion_material.html'
    template = get_template(ruta_tamplate)
    mate = get_object_or_404(Materiales, pk=id)
    context = {'material': mate}
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response
