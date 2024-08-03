from django.core.paginator import Paginator

def paginador_general(request,lista_model):
    pagina = request.GET.get('page',1) #no cambiar de uno, 
    try:
        paginador = Paginator(lista_model,10)#cambiar para aumentar la cantidad que se va mostrar
        paginador_model=paginador.page(pagina)
    except :
        paginador_model= paginador.page(1)
    return paginador_model