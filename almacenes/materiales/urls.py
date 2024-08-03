from django.urls import path
from .views import crear_categoria, crear_material, listado_material,informacion_material, softDelete, editar_material, inprimir
urlpatterns = [
    path('crear_categoria', crear_categoria, name='crear_categoria'),
      path('crear_material', crear_material, name='crear_material'), 

    path('<int:id_categoria>', listado_material, name='categorias_por_id'),  #ruta para listar los prodcutos por categoria  
    path('informacion/<int:id_material>',informacion_material, name='informacion_material' ),
     path('eliminar/<int:id_material>/<int:id_categoria>',softDelete, name='eliminar' ),
      path('editar_material/<int:id_material>',editar_material, name='editar_material' ),

      path('imprimi/<int:id>', inprimir, name='imprimir' )
]