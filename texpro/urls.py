from django.contrib import admin
from django.urls import path
from main.views import mostrar_index, registrar_usuario, login_usuario, cerrar_sesion, mostrar_quienes_somos, mostrar_conoce_texpro, mostrar_contacto
from pedidos.views import mostrar_listado_pedidos, crear_pedido, editar_pedido, eliminar_pedido, obtener_pedido

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mostrar_index, name='index'),
    path('nosotros', mostrar_quienes_somos, name='quienes_somos'),
    path('conoce_texpro', mostrar_conoce_texpro, name='conoce_texpro'),
    path('contacto', mostrar_contacto, name='contacto'),
    path('usuarios/registro', registrar_usuario),
    path('usuarios/login', login_usuario, name='login'),
    path('usuarios/logout', cerrar_sesion, name='cerrar_sesion'),
    path('pedidos/', mostrar_listado_pedidos, name='listado_pedidos'),
    path('pedidos/crear', crear_pedido),
    path('pedidos/editar/<int:id>', editar_pedido),
    path('pedidos/detalle/<int:id>', obtener_pedido),
    path('pedidos/eliminar/<int:id>', eliminar_pedido)
]
