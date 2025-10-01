from django.contrib import admin
from productos.models import Producto, ProductoMedida, EstadoProducto, Medida

# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Producto, ProductoAdmin)

class ProductoMedidaAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProductoMedida, ProductoMedidaAdmin)

class EstadoProductoAdmin(admin.ModelAdmin):
    pass

admin.site.register(EstadoProducto, EstadoProductoAdmin)

class MedidaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Medida, MedidaAdmin)