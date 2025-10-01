from django.contrib import admin
from pedidos.models import Pedido, EstadoPago, EstadoPedido, Cliente
# Register your models here.

class PedidoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pedido, PedidoAdmin)

class EstadoPagoAdmin(admin.ModelAdmin):
    pass

admin.site.register(EstadoPago, EstadoPagoAdmin)

class EstadoPedidoAdmin(admin.ModelAdmin):
    pass

admin.site.register(EstadoPedido, EstadoPedidoAdmin)

class ClienteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cliente, ClienteAdmin)