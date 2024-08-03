from django.urls import path, include 
from .views  import login_sistema, crear_oficinas,Crear_unidad_secretaria,logout_view,crear_unidad_listar,oficinas_listar, creando_usuario, listando_usuarios, crear_secretaria_listar,soft_delete, activar_cuenta, desactivar_cuenta, actulizar_cuenta_usuario
urlpatterns = [

    path("", login_sistema, name="login"),
    path("creando_usuarios", creando_usuario, name="creando_usuarios"),
    path('listando_usuarios',listando_usuarios,name='listando_usuarios' ),
    path('crear_secretaria_listar',crear_secretaria_listar,name='crear_secretaria_listar' ),
    path('eliminar/<int:id>', soft_delete, name='eliminar_cuenta') ,
    path('activar_cuenta/<int:id>', activar_cuenta, name='activar_cuenta') ,
    path('desactivar_cuenta/<int:id>', desactivar_cuenta, name='desactivar_cuenta') ,
    path('actulizar_cuenta_usuario/<int:id_usuario>/<int:id_persona>', actulizar_cuenta_usuario, name='actulizar_cuenta_usuario') ,
    path("logout", logout_view, name='logout'),
    path("unidad",crear_unidad_listar , name='unidad' ),
    path('oficinas/<int:id_unidad>',oficinas_listar, name='oficinas'),
    path('crear_oficinas',crear_oficinas, name='crear_oficinas'),
    path('Crear_unidad_secretaria', Crear_unidad_secretaria, name='Crear_unidad_secretaria')
]