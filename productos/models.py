from django.db import models
from pedidos.models import Pedido

class Medida(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    unidad = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.nombre

class EstadoProducto(models.Model):
    nombre = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=False)
    precio_unitario = models.PositiveIntegerField(blank=False, null=False)
    cantidad = models.PositiveIntegerField(default=1, blank=False, null=False)
    estado_producto = models.ForeignKey(EstadoProducto, on_delete=models.CASCADE, related_name='estados_productos')
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pedidos')

    def __str__(self):
        return f"Producto: {self.nombre} | {self.pedido}"
    
class ProductoMedida(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='productos')
    medidas = models.ForeignKey(Medida, on_delete=models.CASCADE, related_name='medidas')
    longitud = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return f"Producto: {self.producto} | Medida: {self.medidas} {self.longitud} {self.medidas.unidad} "