from django.contrib import admin
from django.urls import path
from main.views import mostrar_index, registrar_usuario, login_usuario, cerrar_sesion
from pedidos.views import mostrar_listado_pedidos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mostrar_index, name='index'),
    path('usuarios/registro', registrar_usuario),
    path('usuarios/login', login_usuario, name='login'),
    path('usuarios/logout', cerrar_sesion, name='cerrar_sesion'),
    path('pedidos/', mostrar_listado_pedidos),
    # path('pedidos/crear', crear_pedido),
    # path('pedidos/editar', editar_pedido),
    # path('pedidos/obtener', obtener_pedido),
    # path('pedidos/eliminar', eliminar_pedido),
    # path('productos/editar', editar_producto),
    # path('productos/eliminar', eliminar_producto),
    # path('medidas/', mostrar_listado_medidas),
    # path('medidas/agregar', agregar_medida),
    # path('medidas/editar', editar_medida)
]
